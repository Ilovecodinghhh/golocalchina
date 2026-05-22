"""User, TouristProfile, GuideProfile models — Path B compliant.
Compatible with both SQLite and PostgreSQL."""
import enum
import uuid
from datetime import datetime, date
from typing import Optional
from sqlalchemy import String, Enum, Date, SmallInteger, Integer, Numeric, Text, ForeignKey, Boolean, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base, TimestampMixin, UUIDMixin


class UserRole(str, enum.Enum):
    tourist = "tourist"
    guide = "guide"
    admin = "admin"


class UserStatus(str, enum.Enum):
    pending = "pending"
    active = "active"
    suspended = "suspended"
    deleted = "deleted"


class KYCStatus(str, enum.Enum):
    unsubmitted = "unsubmitted"
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class User(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "users"

    email: Mapped[Optional[str]] = mapped_column(String(255), unique=True, nullable=True)
    phone_e164: Mapped[Optional[str]] = mapped_column(String(20), unique=True, nullable=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="pending")
    locale: Mapped[str] = mapped_column(String(10), default="en-US")

    tourist_profile: Mapped[Optional["TouristProfile"]] = relationship(back_populates="user", uselist=False)
    guide_profile: Mapped[Optional["GuideProfile"]] = relationship(back_populates="user", uselist=False)


class TouristProfile(Base, TimestampMixin):
    __tablename__ = "tourist_profiles"

    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), primary_key=True)
    display_name: Mapped[str] = mapped_column(String(80), nullable=False)
    nationality: Mapped[Optional[str]] = mapped_column(String(2))
    preferred_currency: Mapped[str] = mapped_column(String(3), default="USD")
    preferred_languages: Mapped[Optional[str]] = mapped_column(JSON, default=[])
    avatar_url: Mapped[Optional[str]] = mapped_column(Text)

    user: Mapped["User"] = relationship(back_populates="tourist_profile")


class GuideProfile(Base, TimestampMixin):
    __tablename__ = "guide_profiles"

    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), primary_key=True)
    legal_name: Mapped[str] = mapped_column(String(120), nullable=False)
    display_name: Mapped[str] = mapped_column(String(80), nullable=False)
    guide_license_no: Mapped[str] = mapped_column(String(40), unique=True, nullable=False)
    guide_license_issuer: Mapped[str] = mapped_column(String(120), nullable=False)
    guide_license_expires_on: Mapped[Optional[str]] = mapped_column(String(10))
    kyc_status: Mapped[str] = mapped_column(String(20), default="unsubmitted")
    languages: Mapped[Optional[str]] = mapped_column(JSON, default=[])
    service_cities: Mapped[Optional[str]] = mapped_column(JSON, default=[])
    specialties: Mapped[Optional[str]] = mapped_column(JSON, default=[])
    bio: Mapped[Optional[str]] = mapped_column(Text)
    avatar_url: Mapped[Optional[str]] = mapped_column(Text)
    default_rate_cny: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    rating_avg: Mapped[float] = mapped_column(Numeric(3, 2), default=0)
    rating_count: Mapped[int] = mapped_column(Integer, default=0)
    # Guide's payment info (tourist pays guide directly)
    alipay_qr_url: Mapped[Optional[str]] = mapped_column(Text)
    wechat_pay_qr_url: Mapped[Optional[str]] = mapped_column(Text)
    accepts_cash: Mapped[bool] = mapped_column(Boolean, default=True)
    payment_note: Mapped[Optional[str]] = mapped_column(String(255))

    user: Mapped["User"] = relationship(back_populates="guide_profile")
