"""GuideListing + AvailabilitySlot."""
from __future__ import annotations

import enum
import uuid
from datetime import date, datetime, time
from decimal import Decimal
from typing import Optional

from geoalchemy2 import Geography
from sqlalchemy import (
    ARRAY, CHAR, Boolean, Date, DateTime, Enum, ForeignKey, Integer, Numeric,
    String, Text, Time, func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class ListingStatus(str, enum.Enum):
    draft = "draft"
    published = "published"
    paused = "paused"
    archived = "archived"


class GuideListing(Base, TimestampMixin):
    __tablename__ = "guide_listings"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    guide_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("guide_profiles.user_id", ondelete="CASCADE"),
        nullable=False, index=True)

    title: Mapped[str] = mapped_column(String(140), nullable=False)
    summary: Mapped[Optional[str]] = mapped_column(Text)
    description: Mapped[Optional[str]] = mapped_column(Text)

    languages: Mapped[list[str]] = mapped_column(
        ARRAY(String(10)), nullable=False, server_default="{}")
    cities: Mapped[list[str]] = mapped_column(
        ARRAY(String(80)), nullable=False, server_default="{}")
    # Geo for radius search (lat/lng of typical meet-up point)
    service_center: Mapped[Optional[str]] = mapped_column(
        Geography(geometry_type="POINT", srid=4326))
    service_radius_km: Mapped[int] = mapped_column(Integer, default=20, server_default="20")

    hourly_price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    half_day_price: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 2))
    full_day_price: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 2))
    currency: Mapped[str] = mapped_column(CHAR(3), nullable=False, default="CNY")

    max_party_size: Mapped[int] = mapped_column(Integer, default=8, server_default="8")
    instant_book: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false")

    status: Mapped[ListingStatus] = mapped_column(
        Enum(ListingStatus, name="listing_status", create_type=False),
        nullable=False, default=ListingStatus.draft)

    guide: Mapped["GuideProfile"] = relationship(back_populates="listings")  # noqa: F821
    slots: Mapped[list["AvailabilitySlot"]] = relationship(
        back_populates="listing", cascade="all, delete-orphan")


class AvailabilitySlot(Base, TimestampMixin):
    __tablename__ = "availability_slots"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    listing_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("guide_listings.id", ondelete="CASCADE"),
        nullable=False, index=True)
    slot_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    start_time: Mapped[time] = mapped_column(Time, nullable=False)
    end_time: Mapped[time] = mapped_column(Time, nullable=False)
    is_booked: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false")

    listing: Mapped["GuideListing"] = relationship(back_populates="slots")
