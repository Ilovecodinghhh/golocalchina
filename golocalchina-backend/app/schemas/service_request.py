"""Service-request (Path B replacement for booking) schemas.

Note: `quoted_price` is NOT accepted from requester; it is set by guide on accept.
"""
from __future__ import annotations

import uuid
from datetime import date, datetime, time
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.models.connection import RequestStatus


class ServiceRequestCreate(BaseModel):
    """Submitted by the requester (foreign visitor) — proposes a meeting."""

    listing_id: uuid.UUID
    service_date: date
    start_time: time
    end_time: time
    party_size: int = Field(default=1, ge=1, le=50)
    meeting_point: Optional[str] = Field(default=None, max_length=255)
    requester_message: Optional[str] = Field(default=None, max_length=2000)


class GuideAcceptRequest(BaseModel):
    """Sent by the guide to accept and quote a price.

    Path B: price is set by the guide here. The platform must not pre-compute
    or override this value (independent-contractor posture).
    """

    quoted_price: Decimal = Field(gt=0)
    currency: str = Field(default="CNY", min_length=3, max_length=3)
    guide_response: Optional[str] = Field(default=None, max_length=2000)


class CancelRequest(BaseModel):
    reason: str = Field(min_length=1, max_length=500)


class ServiceRequestOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    requester_id: uuid.UUID
    guide_id: uuid.UUID
    listing_id: uuid.UUID
    service_date: date
    start_time: time
    end_time: time
    party_size: int
    meeting_point: Optional[str]
    requester_message: Optional[str]
    guide_response: Optional[str]
    quoted_price: Decimal
    currency: str
    platform_commission: Decimal
    status: RequestStatus
    accepted_at: Optional[datetime]
    completed_at: Optional[datetime]
