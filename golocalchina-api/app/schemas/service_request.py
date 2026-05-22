"""Service request (connection request) schemas — no platform payment."""
from typing import Optional
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import date


class CreateServiceRequest(BaseModel):
    """Tourist requests to connect with a guide. Payment is direct between tourist & guide."""
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
    quoted_amount: float    # Guide's price (reference only)
    quoted_currency: str
    status: str

    model_config = {"from_attributes": True}
