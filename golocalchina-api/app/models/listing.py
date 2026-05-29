"""GuideListing — guide-authored, guide-owned. Compatible with SQLite + PostgreSQL."""
import enum
from typing import Optional
from sqlalchemy import String, Text, Numeric, SmallInteger, Integer, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, UUIDMixin, TimestampMixin


class GuideListing(Base, UUIDMixin, TimestampMixin):
    """A guide's service offering. Authored and owned by the guide, not by the platform."""
    __tablename__ = "guide_listings"

    guide_user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(160), nullable=False)
    summary: Mapped[str] = mapped_column(String(500), nullable=False)
    description_md: Mapped[str] = mapped_column(Text, nullable=False)
    city: Mapped[str] = mapped_column(String(80), nullable=False)
    languages: Mapped[Optional[str]] = mapped_column(JSON, default=[])
    price_amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    price_currency: Mapped[str] = mapped_column(String(3), default="CNY")
    price_unit: Mapped[str] = mapped_column(String(20), default="per_half_day")
    max_group_size: Mapped[int] = mapped_column(SmallInteger, default=8)
    tags: Mapped[Optional[str]] = mapped_column(JSON, default=[])
    cover_image_url: Mapped[Optional[str]] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(20), default="draft")
    
    # New fields for images, map links, and engagement metrics
    images: Mapped[Optional[str]] = mapped_column(JSON, default=[])  # Additional image URLs
    map_links: Mapped[Optional[str]] = mapped_column(JSON, default=[])  # Map links (Google Maps, Baidu Maps, etc.)
    views: Mapped[int] = mapped_column(Integer, default=0)  # View count
    likes: Mapped[int] = mapped_column(Integer, default=0)  # Like count
