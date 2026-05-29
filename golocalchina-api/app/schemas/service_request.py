"""Service request schemas — connection request between tourist and guide."""
from typing import Optional
from pydantic import BaseModel, Field
from datetime import date


class CreateServiceRequest(BaseModel):
    """Tourist requests to connect with a guide."""
    guide_user_id: str
    listing_id: Optional[str] = None
    service_date: date
    service_time_hour: Optional[int] = None
    party_size: int = Field(default=1, ge=1, le=30)
    language: str = "en"
    tourist_notes: Optional[str] = None
    quoted_amount: Optional[float] = None
    quoted_currency: str = "CNY"


class ServiceRequestResponse(BaseModel):
    id: str
    tourist_user_id: str
    guide_user_id: str
    listing_id: Optional[str]
    service_date: str
    quoted_amount: float
    quoted_currency: str
    status: str

    model_config = {"from_attributes": True}
