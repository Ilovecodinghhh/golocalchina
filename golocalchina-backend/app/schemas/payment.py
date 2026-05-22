"""Payment schemas — reflect PSP (Airwallex) state.

We do NOT expose any platform-held balance. The PSP is merchant-of-record on
the guide side via destination charges; this app only records the reference.
"""
from __future__ import annotations

import uuid
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.models.connection import PaymentStatus


class PaymentIntentCreate(BaseModel):
    request_id: uuid.UUID


class PaymentIntentOut(BaseModel):
    """Client-side payment-intent stub returned to the requester."""

    payment_id: uuid.UUID
    psp: str
    psp_intent_id: str
    client_secret: str
    amount: Decimal
    currency: str
    destination_account: str  # guide's PSP merchant account ID


class PaymentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    request_id: uuid.UUID
    psp: str
    psp_payment_id: Optional[str]
    psp_intent_id: Optional[str]
    psp_destination_account: Optional[str]
    amount: Decimal
    currency: str
    status: PaymentStatus
