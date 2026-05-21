"""Guide search + detail schemas."""
from typing import Optional
from pydantic import BaseModel, Field
from uuid import UUID


class GuideSearchParams(BaseModel):
    city: Optional[str] = None
    language: Optional[str] = None
    specialty: Optional[str] = None
    date: Optional[str] = None
    min_rating: Optional[float] = None
    max_price_cny: Optional[float] = None
    page: int = Field(default=1, ge=1)
    per_page: int = Field(default=20, ge=1, le=50)


class GuideListItem(BaseModel):
    user_id: UUID
    display_name: str
    languages: list[str]
    service_cities: list[str]
    specialties: list[str]
    rating_avg: float
    rating_count: int
    default_rate_cny: float
    avatar_url: Optional[str] = None
    bio: Optional[str] = None

    model_config = {"from_attributes": True}


class GuideDetail(GuideListItem):
    guide_license_no: str
    guide_license_issuer: str
    kyc_status: str
    listings: list[dict] = []


class GuideSearchResponse(BaseModel):
    guides: list[GuideListItem]
    total: int
    page: int
    per_page: int
