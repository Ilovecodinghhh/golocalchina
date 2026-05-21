"""Service request (connection request) schemas — Path B naming."""
from typing import Optional
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import date


class CreateServiceRequest(BaseModel):
    """Tourist requests to connect with a guide. NOT a 'tour booking'."""
    listing_id: UUID
    service_date: date
    party_size: int = Field(default=1, ge=1, le=30)
    language: str = "en"
    tourist_notes: Optional[str] = None


class ServiceRequestResponse(BaseModel):
    id: UUID
    tourist_user_id: UUID
    guide_user_id: UUID
    listing_id: Optional[UUID]
    service_date: date
    quoted_amount: float
    quoted_currency: str
    platform_fee_amount: float  # 信息服务费
    guide_payout_amount: float
    status: str

    model_config = {"from_attributes": True}
