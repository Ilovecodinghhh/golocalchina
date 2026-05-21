"""Consent schemas."""
from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.models.consent import ConsentPurpose, LawfulBasis


class ConsentGrantRequest(BaseModel):
    purpose: ConsentPurpose
    policy_version: str
    lawful_basis: LawfulBasis = LawfulBasis.consent
    jurisdiction: str = "CN"


class ConsentRecordOut(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    purpose: ConsentPurpose
    policy_version: str
    lawful_basis: LawfulBasis
    jurisdiction: str
    granted_at: datetime
    withdrawn_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
