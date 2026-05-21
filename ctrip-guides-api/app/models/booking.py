"""ServiceRequest + Payment + Payout + Review — Path B compliant.
ServiceRequest = tourist requests to connect with a guide (NOT a "tour booking")."""
import enum
import uuid
from datetime import datetime, date
from typing import Optional
from sqlalchemy import String, Enum, Text, Numeric, SmallInteger, Integer, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, UUIDMixin, TimestampMixin


class RequestStatus(str, enum.Enum):
    pending = "pending"
    accepted = "accepted"
    paid = "paid"
    confirmed = "confirmed"
    in_progress = "in_progress"
    completed = "completed"
    cancelled_by_tourist = "cancelled_by_tourist"
    cancelled_by_guide = "cancelled_by_guide"
    refunded = "refunded"
    disputed = "disputed"


class PaymentStatus(str, enum.Enum):
    initiated = "initiated"
    authorized = "authorized"
    captured = "captured"
    failed = "failed"
    refunded = "refunded"


class ServiceRequest(Base, UUIDMixin, TimestampMixin):
    """Tourist → Guide connection request. Platform facilitates, does NOT organize."""
    __tablename__ = "service_requests"

    tourist_user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    guide_user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    listing_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("guide_listings.id"))
    service_date: Mapped[date] = mapped_column(Date, nullable=False)
    party_size: Mapped[int] = mapped_column(SmallInteger, default=1)
    language: Mapped[str] = mapped_column(String(10), nullable=False)
    tourist_notes: Mapped[Optional[str]] = mapped_column(Text)
    # Pricing snapshot — guide-set price at time of request
    quoted_amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    quoted_currency: Mapped[str] = mapped_column(String(3), nullable=False)
    # 信息服务费 (Information Service Fee) — NOT commission
    platform_fee_pct: Mapped[float] = mapped_column(Numeric(5, 2), default=12.00)
    platform_fee_amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    guide_payout_amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    status: Mapped[RequestStatus] = mapped_column(Enum(RequestStatus), default=RequestStatus.pending)


class Review(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "reviews"

    service_request_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("service_requests.id"))
    reviewer_user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    target_user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    stars: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    text: Mapped[Optional[str]] = mapped_column(Text)
