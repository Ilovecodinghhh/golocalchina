"""ServiceRequest + Review — compatible with SQLite + PostgreSQL."""
from typing import Optional
from sqlalchemy import String, Text, Numeric, SmallInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, UUIDMixin, TimestampMixin


class ServiceRequest(Base, UUIDMixin, TimestampMixin):
    """Tourist → Guide connection request. Payment is direct between tourist and guide."""
    __tablename__ = "service_requests"

    tourist_user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False)
    guide_user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False)
    listing_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("guide_listings.id"))
    service_date: Mapped[str] = mapped_column(String(10), nullable=False)
    party_size: Mapped[int] = mapped_column(SmallInteger, default=1)
    language: Mapped[str] = mapped_column(String(10), nullable=False)
    tourist_notes: Mapped[Optional[str]] = mapped_column(Text)
    quoted_amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    quoted_currency: Mapped[str] = mapped_column(String(3), nullable=False)
    status: Mapped[str] = mapped_column(String(30), default="pending")


class Review(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "reviews"

    service_request_id: Mapped[str] = mapped_column(String(36), ForeignKey("service_requests.id"))
    reviewer_user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"))
    target_user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"))
    stars: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    text: Mapped[Optional[str]] = mapped_column(Text)
