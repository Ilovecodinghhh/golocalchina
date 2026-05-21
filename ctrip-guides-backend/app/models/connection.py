"""ServiceRequest + Settlement ORM models.

Path B compliance posture (Legal-reviewed pattern):
- "ServiceRequest" replaces "Booking" → information-intermediary semantics.
- "Settlement" replaces "Payout" → records direct PSP→guide transfer (Airwallex
  destination charges); platform never holds funds. The `psp_transfer_id`
  column is the PSP-side authoritative record; this table is only a *reflection*
  for reconciliation, not a ledger.
- `quoted_price` is supplied BY THE GUIDE in the accept-step, not computed by
  platform. See app/api/v1/service_requests.py for the contract.
- `platform_commission` is a separately-invoiced intermediary fee, NOT
  principal revenue. The full `requester_amount` is captured by the PSP with
  guide as merchant of record on a destination charge; commission is split
  off and routed to the platform's PSP sub-account as service-fee.
- NO columns named `platform_balance`, `escrow`, `held_funds`, `wallet`.
"""
from __future__ import annotations

import enum
import uuid
from datetime import date, datetime, time
from decimal import Decimal
from typing import Optional

from sqlalchemy import (
    CHAR,
    CheckConstraint,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    Time,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class RequestStatus(str, enum.Enum):
    pending = "pending"            # requester submitted; guide has not responded
    accepted = "accepted"          # guide accepted with a quoted price
    paid = "paid"                  # PSP captured requester payment (direct to guide MoR)
    confirmed = "confirmed"        # both parties confirmed meeting details
    in_progress = "in_progress"
    completed = "completed"
    cancelled_by_requester = "cancelled_by_requester"
    cancelled_by_guide = "cancelled_by_guide"
    refunded = "refunded"
    disputed = "disputed"


class PaymentStatus(str, enum.Enum):
    initiated = "initiated"
    authorized = "authorized"
    captured = "captured"
    failed = "failed"
    refunded = "refunded"
    partially_refunded = "partially_refunded"


class SettlementStatus(str, enum.Enum):
    """Status of direct PSP→guide transfer (NOT a platform-held balance)."""
    scheduled = "scheduled"
    processing = "processing"
    paid = "paid"
    failed = "failed"
    on_hold = "on_hold"  # PSP-side hold (e.g., KYC reverification), not platform


class ServiceRequest(Base, TimestampMixin):
    """A discovery + connection record between a requester and a guide.

    Per Path B: this is NOT a tour booking. The platform documents that the
    parties were introduced and that direct contracting occurred between them.
    """

    __tablename__ = "service_requests"
    __table_args__ = (
        CheckConstraint("end_time > start_time", name="service_requests_time_chk"),
        CheckConstraint("party_size >= 1", name="service_requests_party_chk"),
        CheckConstraint(
            "quoted_price >= 0 AND platform_commission >= 0",
            name="service_requests_money_chk",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    requester_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    guide_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("guide_profiles.user_id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    listing_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("guide_listings.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    service_date: Mapped[date] = mapped_column(Date, nullable=False)
    start_time: Mapped[time] = mapped_column(Time, nullable=False)
    end_time: Mapped[time] = mapped_column(Time, nullable=False)
    party_size: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    meeting_point: Mapped[Optional[str]] = mapped_column(String(255))
    requester_message: Mapped[Optional[str]] = mapped_column(Text)
    guide_response: Mapped[Optional[str]] = mapped_column(Text)

    # GUIDE-SET price (set in accept step). Platform MUST NOT compute.
    quoted_price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    currency: Mapped[str] = mapped_column(CHAR(3), nullable=False, default="CNY")
    # Separately-invoiced platform commission (intermediary fee, not principal).
    platform_commission: Mapped[Decimal] = mapped_column(
        Numeric(12, 2), nullable=False, server_default="0"
    )

    status: Mapped[RequestStatus] = mapped_column(
        Enum(RequestStatus, name="request_status", create_type=False),
        nullable=False,
        default=RequestStatus.pending,
        index=True,
    )
    cancellation_reason: Mapped[Optional[str]] = mapped_column(Text)
    accepted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    payments: Mapped[list["Payment"]] = relationship(
        back_populates="request", cascade="all, delete-orphan"
    )
    settlements: Mapped[list["Settlement"]] = relationship(
        back_populates="request", cascade="all, delete-orphan"
    )


class Payment(Base, TimestampMixin):
    """PSP-side payment record (requester → guide via destination charge).

    The PSP (Airwallex) is the merchant-of-record on the guide side; this row
    is a *reflection* of the PSP intent, never a platform balance.
    """

    __tablename__ = "payments"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    request_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("service_requests.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    psp: Mapped[str] = mapped_column(String(20), nullable=False, default="airwallex")
    psp_payment_id: Mapped[Optional[str]] = mapped_column(String(80), unique=True)
    psp_intent_id: Mapped[Optional[str]] = mapped_column(String(80))
    # Guide is destination merchant on Airwallex side:
    psp_destination_account: Mapped[Optional[str]] = mapped_column(String(80))

    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    currency: Mapped[str] = mapped_column(CHAR(3), nullable=False)
    status: Mapped[PaymentStatus] = mapped_column(
        Enum(PaymentStatus, name="payment_status", create_type=False),
        nullable=False,
        default=PaymentStatus.initiated,
        index=True,
    )
    raw_response: Mapped[Optional[dict]] = mapped_column(JSONB)
    authorized_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    captured_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    request: Mapped["ServiceRequest"] = relationship(back_populates="payments")


class Settlement(Base, TimestampMixin):
    """Reflection of a direct PSP→guide transfer for one service_request.

    Renamed from `Payout` to make clear this is NOT a platform-initiated
    payout from a held balance. The actual money movement is PSP-managed
    via destination-charge settlement on the merchant-of-record (guide).
    """

    __tablename__ = "settlements"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    request_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("service_requests.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    guide_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("guide_profiles.user_id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    currency: Mapped[str] = mapped_column(CHAR(3), nullable=False)
    psp_transfer_id: Mapped[Optional[str]] = mapped_column(String(80), unique=True)
    status: Mapped[SettlementStatus] = mapped_column(
        Enum(SettlementStatus, name="settlement_status", create_type=False),
        nullable=False,
        default=SettlementStatus.scheduled,
        index=True,
    )
    scheduled_for: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    paid_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    request: Mapped["ServiceRequest"] = relationship(back_populates="settlements")
