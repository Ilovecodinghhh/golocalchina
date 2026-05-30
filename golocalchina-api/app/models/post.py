"""TouristPost — tourists can create posts with text and images."""
from typing import Optional
from sqlalchemy import String, Text, Boolean, ForeignKey, JSON, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, UUIDMixin, TimestampMixin


class TouristPost(Base, UUIDMixin, TimestampMixin):
    """A post created by a tourist. Can be marked as done."""
    __tablename__ = "tourist_posts"

    author_user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    images: Mapped[Optional[str]] = mapped_column(JSON, default=[])  # List of image URLs
    is_done: Mapped[bool] = mapped_column(Boolean, default=False)
    view_count: Mapped[int] = mapped_column(Integer, default=0)
    like_count: Mapped[int] = mapped_column(Integer, default=0)


class PostLike(Base, UUIDMixin, TimestampMixin):
    """Tracks which users liked which posts."""
    __tablename__ = "post_likes"

    post_id: Mapped[str] = mapped_column(String(36), ForeignKey("tourist_posts.id"), nullable=False)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False)
