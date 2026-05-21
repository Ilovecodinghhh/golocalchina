"""GuideListing + AvailabilitySlot — guide-authored, guide-owned content.
Path B: These are NOT tours/packages. They are service offerings authored by the guide."""
import enum
import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Enum, Text, Numeric, SmallInteger, Boolean, ARRAY, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, UUIDMixin, TimestampMixin


class ListingStatus(str, enum.Enum):
    draft = "draft"
    published = "published"
    paused = "paused"
    archived = "archived"


class GuideListing(Base, UUIDMixin, TimestampMixin):
    """A guide's service offering. Authored and owned by the guide, not by the platform."""
    __tablename__ = "guide_listings"

    guide_user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(160), nullable=False)
    summary: Mapped[str] = mapped_column(String(500), nullable=False)
    description_md: Mapped[str] = mapped_column(Text, nullable=False)
    city: Mapped[str] = mapped_column(String(80), nullable=False)
    languages: Mapped[list] = mapped_column(ARRAY(String(10)), default=[])
    # Guide-set pricing (platform does NOT control pricing)
    price_amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    price_currency: Mapped[str] = mapped_column(String(3), default="CNY")
    price_unit: Mapped[str] = mapped_column(String(20), default="per_half_day")
    max_group_size: Mapped[int] = mapped_column(SmallInteger, default=8)
    tags: Mapped[list] = mapped_column(ARRAY(Text), default=[])
    cover_image_url: Mapped[Optional[str]] = mapped_column(Text)
    status: Mapped[ListingStatus] = mapped_column(Enum(ListingStatus), default=ListingStatus.draft)
