"""Consent records — PIPL Art. 14 / 23 / 39, GDPR Art. 7 + Recital 32.

Each row is one user's grant (or withdrawal) of one purpose under one
specific policy version. Separate consents are stored as separate rows
(NOT a bitmask) so the "specific & informed" requirement is auditable.
"""
from __future__ import annotations

import enum
import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import (
    CHAR,
    CheckConstraint,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    String,
    func,
)
from sqlalchemy.dialects.postgresql import INET, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class ConsentPurpose(str, enum.Enum):
    """Discrete consent purposes (PIPL Art. 14 specificity requirement)."""

    account_processing = "account_processing"           # base lawful processing
    sensitive_pi = "sensitive_pi"                       # PIPL Art. 28 separate consent
    cross_border_transfer = "cross_border_transfer"     # PIPL Art. 39
    marketing_email = "marketing_email"
    marketing_sms = "marketing_sms"
    third_party_sharing = "third_party_sharing"         # PIPL Art. 23
    analytics_cookies = "analytics_cookies"             # GDPR ePrivacy


class LawfulBasis(str, enum.Enum):
    """GDPR Art. 6 lawful bases (mapped to PIPL Art. 13)."""

    consent = "consent"
    contract = "contract"
    legal_obligation = "legal_obligation"
    vital_interests = "vital_interests"
    public_task = "public_task"
    legitimate_interests = "legitimate_interests"


class ConsentRecord(Base):
    """Immutable consent grant/withdrawal record.

    Append-only: a withdrawal is recorded by setting `withdrawn_at` on the
    existing row OR by inserting a new row with the same (user_id, purpose);
    we always read MAX(granted_at) to determine current state.
    """

    __tablename__ = "consent_records"
    __table_args__ = (
        CheckConstraint(
            "withdrawn_at IS NULL OR withdrawn_at >= granted_at",
            name="consent_records_chronology_chk",
        ),
        Index("consent_records_user_purpose_idx", "user_id", "purpose"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    purpose: Mapped[ConsentPurpose] = mapped_column(
        Enum(ConsentPurpose, name="consent_purpose", create_type=False),
        nullable=False,
    )
    policy_version: Mapped[str] = mapped_column(String(40), nullable=False)
    lawful_basis: Mapped[LawfulBasis] = mapped_column(
        Enum(LawfulBasis, name="lawful_basis", create_type=False),
        nullable=False,
        default=LawfulBasis.consent,
    )
    jurisdiction: Mapped[str] = mapped_column(
        CHAR(2),
        nullable=False,
        default="CN",
        comment="ISO 3166-1 alpha-2 of the data subject at time of grant",
    )
    granted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    withdrawn_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    granted_from_ip: Mapped[Optional[str]] = mapped_column(INET)
    user_agent: Mapped[Optional[str]] = mapped_column(String(500))
