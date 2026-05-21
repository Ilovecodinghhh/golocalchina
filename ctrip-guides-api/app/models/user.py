"""User, TouristProfile, GuideProfile models — Path B compliant."""
import enum
import uuid
from datetime import datetime, date
from typing import Optional
from sqlalchemy import String, Enum, Date, SmallInteger, Integer, Numeric, Text, ARRAY, ForeignKey, Boolean
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
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False)
    status: Mapped[UserStatus] = mapped_column(Enum(UserStatus), default=UserStatus.pending)
    locale: Mapped[str] = mapped_column(String(10), default="en-US")

    # Relationships
    tourist_profile: Mapped[Optional["TouristProfile"]] = relationship(back_populates="user", uselist=False)
    guide_profile: Mapped[Optional["GuideProfile"]] = relationship(back_populates="user", uselist=False)


class TouristProfile(Base, TimestampMixin):
    __tablename__ = "tourist_profiles"

    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    display_name: Mapped[str] = mapped_column(String(80), nullable=False)
    nationality: Mapped[Optional[str]] = mapped_column(String(2))
    preferred_currency: Mapped[str] = mapped_column(String(3), default="USD")
    preferred_languages: Mapped[list] = mapped_column(ARRAY(String(10)), default=[])
    avatar_url: Mapped[Optional[str]] = mapped_column(Text)

    user: Mapped["User"] = relationship(back_populates="tourist_profile")


class GuideProfile(Base, TimestampMixin):
    __tablename__ = "guide_profiles"

    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    legal_name: Mapped[str] = mapped_column(String(120), nullable=False)
    display_name: Mapped[str] = mapped_column(String(80), nullable=False)
    # 导游证 fields
    guide_license_no: Mapped[str] = mapped_column(String(40), unique=True, nullable=False)
    guide_license_issuer: Mapped[str] = mapped_column(String(120), nullable=False)
    guide_license_expires_on: Mapped[date] = mapped_column(Date, nullable=False)
    kyc_status: Mapped[KYCStatus] = mapped_column(Enum(KYCStatus), default=KYCStatus.unsubmitted)
    # Service profile
    languages: Mapped[list] = mapped_column(ARRAY(String(10)), default=[])
    service_cities: Mapped[list] = mapped_column(ARRAY(Text), default=[])
    specialties: Mapped[list] = mapped_column(ARRAY(Text), default=[])
    bio: Mapped[Optional[str]] = mapped_column(Text)
    avatar_url: Mapped[Optional[str]] = mapped_column(Text)
    # Guide-set pricing — platform does NOT set prices
    default_rate_cny: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    rating_avg: Mapped[float] = mapped_column(Numeric(3, 2), default=0)
    rating_count: Mapped[int] = mapped_column(Integer, default=0)

    user: Mapped["User"] = relationship(back_populates="guide_profile")
