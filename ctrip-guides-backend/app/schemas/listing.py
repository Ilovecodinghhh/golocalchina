"""Listing schemas (guide-authored marketing artefact, not a tour package)."""
from __future__ import annotations

import uuid
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.models.listing import ListingStatus


class ListingCreate(BaseModel):
    title: str = Field(min_length=3, max_length=140)
    summary: Optional[str] = Field(default=None, max_length=600)
    description: Optional[str] = None
    languages: list[str] = Field(default_factory=list)
    cities: list[str] = Field(default_factory=list)
    hourly_price: Decimal = Field(gt=0)
    half_day_price: Optional[Decimal] = Field(default=None, gt=0)
    full_day_price: Optional[Decimal] = Field(default=None, gt=0)
    currency: str = Field(default="CNY", min_length=3, max_length=3)
    max_party_size: int = Field(default=8, ge=1, le=50)
    instant_book: bool = False
    service_radius_km: int = Field(default=20, ge=1, le=500)


class ListingUpdate(BaseModel):
    title: Optional[str] = None
    summary: Optional[str] = None
    description: Optional[str] = None
    languages: Optional[list[str]] = None
    cities: Optional[list[str]] = None
    hourly_price: Optional[Decimal] = None
    half_day_price: Optional[Decimal] = None
    full_day_price: Optional[Decimal] = None
    max_party_size: Optional[int] = None
    instant_book: Optional[bool] = None
    status: Optional[ListingStatus] = None


class ListingOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    guide_id: uuid.UUID
    title: str
    summary: Optional[str]
    languages: list[str]
    cities: list[str]
    hourly_price: Decimal
    half_day_price: Optional[Decimal]
    full_day_price: Optional[Decimal]
    currency: str
    max_party_size: int
    instant_book: bool
    status: ListingStatus
