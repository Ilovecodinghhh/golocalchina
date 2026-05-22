"""User, RequesterProfile, GuideProfile ORM models.

Path B compliance notes:
- "Tourist" terminology purged per Legal lexicon (PIPL/旅游法 risk reduction).
- Guide profile fields are guide-authored (display_name, bio, languages, home_city).
  Platform does NOT set guide attributes, prices, or schedules → independent
  contractor posture preserved (cf. 劳动合同法 Art. 7; 人社部发〔2021〕56号).
"""
from __future__ import annotations

import enum
import uuid
from datetime import date, datetime
from typing import Optional

from sqlalchemy import (
    ARRAY,
    CHAR,
    CheckConstraint,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import CITEXT, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class UserRole(str, enum.Enum):
    requester = "requester"  # foreign visitor seeking a guide (was: tourist)
    guide = "guide"
    admin = "admin"


class UserStatus(str, enum.Enum):
    pending = "pending"
    active = "active"
    suspended = "suspended"
    deleted = "deleted"


class KycStatus(str, enum.Enum):
    unsubmitted = "unsubmitted"
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class User(Base, TimestampMixin):
    __tablename__ = "users"
    __table_args__ = (
        CheckConstraint(
            "email IS NOT NULL OR phone_e164 IS NOT NULL",
            name="users_contact_chk",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    email: Mapped[Optional[str]] = mapped_column(CITEXT, unique=True)
    phone_e164: Mapped[Optional[str]] = mapped_column(String(20), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, name="user_role", create_type=False), nullable=False
    )
    status: Mapped[UserStatus] = mapped_column(
        Enum(UserStatus, name="user_status", create_type=False),
        nullable=False,
        default=UserStatus.pending,
    )
    locale: Mapped[str] = mapped_column(String(10), nullable=False, default="en-US")
    timezone: Mapped[str] = mapped_column(
        String(64), nullable=False, default="Asia/Shanghai"
    )
    email_verified_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True)
    )
    phone_verified_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True)
    )
    last_login_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    requester_profile: Mapped[Optional["RequesterProfile"]] = relationship(
        back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
    guide_profile: Mapped[Optional["GuideProfile"]] = relationship(
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
        foreign_keys="GuideProfile.user_id",
    )


class RequesterProfile(Base, TimestampMixin):
    """Profile for users in the `requester` role (foreign visitors).

    NB: Renamed from TouristProfile per Path B lexicon. "Tourist" + "booking"
    together implies travel-agency relationship (旅行社条例 Art. 6).
    """

    __tablename__ = "requester_profiles"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    display_name: Mapped[str] = mapped_column(String(80), nullable=False)
    nationality: Mapped[Optional[str]] = mapped_column(CHAR(2))
    preferred_currency: Mapped[str] = mapped_column(
        CHAR(3), nullable=False, default="USD"
    )
    preferred_languages: Mapped[list[str]] = mapped_column(
        ARRAY(String(10)), nullable=False, server_default="{}"
    )
    passport_country: Mapped[Optional[str]] = mapped_column(CHAR(2))
    avatar_url: Mapped[Optional[str]] = mapped_column(Text)
    bio: Mapped[Optional[str]] = mapped_column(Text)

    user: Mapped["User"] = relationship(back_populates="requester_profile")


class GuideProfile(Base, TimestampMixin):
    __tablename__ = "guide_profiles"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    legal_name: Mapped[str] = mapped_column(String(120), nullable=False)
    display_name: Mapped[str] = mapped_column(String(80), nullable=False)

    # 导游证 — mandatory per 旅游法 Art. 38 (only licensed guides may provide service)
    guide_license_no: Mapped[str] = mapped_column(
        String(40), nullable=False, unique=True
    )
    guide_license_issuer: Mapped[str] = mapped_column(String(120), nullable=False)
    guide_license_issued_on: Mapped[date] = mapped_column(Date, nullable=False)
    guide_license_expires_on: Mapped[date] = mapped_column(Date, nullable=False)
    guide_license_scan_url: Mapped[str] = mapped_column(Text, nullable=False)
    id_card_last4: Mapped[str] = mapped_column(CHAR(4), nullable=False)

    kyc_status: Mapped[KycStatus] = mapped_column(
        Enum(KycStatus, name="kyc_status", create_type=False),
        nullable=False,
        default=KycStatus.unsubmitted,
    )
    kyc_reviewed_by: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id")
    )
    kyc_reviewed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True)
    )
    kyc_rejection_reason: Mapped[Optional[str]] = mapped_column(Text)

    # service profile — guide-authored
    spoken_languages: Mapped[list[str]] = mapped_column(
        ARRAY(String(10)), nullable=False, server_default="{}"
    )
    home_city: Mapped[Optional[str]] = mapped_column(String(80))
    bio: Mapped[Optional[str]] = mapped_column(Text)
    avatar_url: Mapped[Optional[str]] = mapped_column(Text)
    average_rating: Mapped[Optional[float]] = mapped_column()
    review_count: Mapped[int] = mapped_column(default=0, server_default="0")

    user: Mapped["User"] = relationship(
        back_populates="guide_profile", foreign_keys=[user_id]
    )
    listings: Mapped[list["GuideListing"]] = relationship(  # noqa: F821
        back_populates="guide", cascade="all, delete-orphan"
    )
