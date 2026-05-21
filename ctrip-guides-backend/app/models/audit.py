"""Audit log — PIPL Art. 51(4), 数据安全法 Art. 27, GDPR Art. 30.

Append-only. Migration revokes UPDATE/DELETE from the application role.
Retention ≥ 3 years (we set default 7 years to be safe under PIPL).
"""
from __future__ import annotations

import enum
import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import INET, JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class AuditAction(str, enum.Enum):
    create = "create"
    read = "read"
    update = "update"
    delete = "delete"
    login = "login"
    logout = "logout"
    consent_grant = "consent_grant"
    consent_withdraw = "consent_withdraw"
    export = "export"               # DSR data export
    erasure = "erasure"             # DSR data erasure
    cross_border_transfer = "cross_border_transfer"


class AuditLog(Base):
    """Immutable record of personal-info access / processing events."""

    __tablename__ = "audit_logs"
    __table_args__ = (
        CheckConstraint(
            "actor_id IS NOT NULL OR actor_kind = 'system'",
            name="audit_logs_actor_chk",
        ),
        Index("audit_logs_subject_idx", "subject_user_id"),
        Index("audit_logs_actor_idx", "actor_id"),
        Index("audit_logs_occurred_at_idx", "occurred_at"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    occurred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    # WHO acted
    actor_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL")
    )
    actor_kind: Mapped[str] = mapped_column(
        String(20), nullable=False, default="user",
        comment="user | admin | system | psp_webhook",
    )
    actor_ip: Mapped[Optional[str]] = mapped_column(INET)

    # ON WHOSE data
    subject_user_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL")
    )

    # WHAT
    action: Mapped[AuditAction] = mapped_column(
        Enum(AuditAction, name="audit_action", create_type=False), nullable=False
    )
    resource_type: Mapped[str] = mapped_column(String(64), nullable=False)
    resource_id: Mapped[Optional[str]] = mapped_column(String(80))

    # WHY (lawful basis under PIPL Art. 13 / GDPR Art. 6)
    purpose: Mapped[str] = mapped_column(String(120), nullable=False)
    lawful_basis: Mapped[str] = mapped_column(String(40), nullable=False)

    # additional context
    request_id: Mapped[Optional[str]] = mapped_column(String(40))
    detail: Mapped[Optional[dict]] = mapped_column(JSONB)
    note: Mapped[Optional[str]] = mapped_column(Text)
