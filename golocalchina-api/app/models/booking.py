"""ServiceRequest + Review — Path B compliant. No platform payment processing.
Tourist pays guide directly (cash, Alipay, WeChat Pay) at time of service."""
import enum
import uuid
from datetime import datetime, date
from typing import Optional
from sqlalchemy import String, Enum, Text, Numeric, SmallInteger, Integer, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, UUIDMixin, TimestampMixin


class RequestStatus(str, enum.Enum):
    pending = "pending"           # tourist submitted, awaiting guide response
    accepted = "accepted"         # guide accepted — tourist and guide arrange meeting
    in_progress = "in_progress"   # service day
    completed = "completed"       # both parties confirm service happened
    cancelled_by_tourist = "cancelled_by_tourist"
    cancelled_by_guide = "cancelled_by_guide"
    no_show = "no_show"


class ServiceRequest(Base, UUIDMixin, TimestampMixin):
    """Tourist → Guide connection request. Platform facilitates, does NOT organize.
    Payment is arranged directly between tourist and guide — platform does not process payments."""
    __tablename__ = "service_requests"

    tourist_user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    guide_user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    listing_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("guide_listings.id"))
    service_date: Mapped[date] = mapped_column(Date, nullable=False)
    party_size: Mapped[int] = mapped_column(SmallInteger, default=1)
    language: Mapped[str] = mapped_column(String(10), nullable=False)
    tourist_notes: Mapped[Optional[str]] = mapped_column(Text)
    # Guide-set price (reference only — payment happens directly between tourist & guide)
    quoted_amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    quoted_currency: Mapped[str] = mapped_column(String(3), nullable=False)
    status: Mapped[RequestStatus] = mapped_column(Enum(RequestStatus), default=RequestStatus.pending)


class Review(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "reviews"

    service_request_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("service_requests.id"))
    reviewer_user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    target_user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    stars: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    text: Mapped[Optional[str]] = mapped_column(Text)
