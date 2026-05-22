"""User / profile schemas."""
from __future__ import annotations

import uuid
from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models.user import KycStatus, UserRole, UserStatus


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    email: Optional[EmailStr]
    phone_e164: Optional[str]
    role: UserRole
    status: UserStatus
    locale: str
    timezone: str


class RequesterProfileOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: uuid.UUID
    display_name: str
    nationality: Optional[str]
    preferred_currency: str
    preferred_languages: list[str]


class GuideProfileOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: uuid.UUID
    display_name: str
    home_city: Optional[str]
    spoken_languages: list[str]
    bio: Optional[str]
    avatar_url: Optional[str]
    average_rating: Optional[float]
    review_count: int
    kyc_status: KycStatus


class GuideProfileCreate(BaseModel):
    legal_name: str = Field(min_length=2, max_length=120)
    display_name: str = Field(min_length=1, max_length=80)
    guide_license_no: str = Field(min_length=4, max_length=40)
    guide_license_issuer: str = Field(min_length=2, max_length=120)
    guide_license_issued_on: date
    guide_license_expires_on: date
    guide_license_scan_url: str
    id_card_last4: str = Field(min_length=4, max_length=4, pattern=r"^[0-9]{4}$")
    spoken_languages: list[str] = Field(default_factory=list)
    home_city: Optional[str] = None
    bio: Optional[str] = None
