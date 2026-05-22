"""Audit logger service — wraps inserts into audit_logs.

Use this everywhere PI is accessed; never write to audit_logs directly.
"""
from __future__ import annotations

import uuid
from typing import Any, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.audit import AuditAction, AuditLog


async def record_audit(
    db: AsyncSession,
    *,
    action: AuditAction,
    resource_type: str,
    purpose: str,
    lawful_basis: str,
    actor_id: Optional[uuid.UUID] = None,
    actor_kind: str = "user",
    actor_ip: Optional[str] = None,
    subject_user_id: Optional[uuid.UUID] = None,
    resource_id: Optional[str] = None,
    request_id: Optional[str] = None,
    detail: Optional[dict[str, Any]] = None,
    note: Optional[str] = None,
) -> AuditLog:
    """Insert an audit log entry.

    NB: Caller MUST NOT update or delete the returned row. The DB role
    used by the app has only INSERT/SELECT on this table (see migration
    20260521_0002_audit_log_append_only.py).
    """
    entry = AuditLog(
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        purpose=purpose,
        lawful_basis=lawful_basis,
        actor_id=actor_id,
        actor_kind=actor_kind,
        actor_ip=actor_ip,
        subject_user_id=subject_user_id,
        request_id=request_id,
        detail=detail,
        note=note,
    )
    db.add(entry)
    await db.flush()
    return entry
