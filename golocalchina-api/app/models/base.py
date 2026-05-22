"""SQLAlchemy declarative base + common mixins. SQLite + PostgreSQL compatible."""
import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, String, event
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class TimestampMixin:
    created_at: Mapped[str] = mapped_column(String(30), default=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: Mapped[str] = mapped_column(String(30), default=lambda: datetime.now(timezone.utc).isoformat(),
                                            onupdate=lambda: datetime.now(timezone.utc).isoformat())


class UUIDMixin:
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
