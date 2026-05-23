"""Guide Listing CRUD — guides create and manage their service offerings."""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.models.listing import GuideListing

router = APIRouter(prefix="/listings", tags=["listings"])


class CreateListing(BaseModel):
    title: str = Field(min_length=5, max_length=160)
    summary: str = Field(min_length=10, max_length=500)
    description_md: str = Field(min_length=20)
    city: str
    languages: list[str] = []
    price_amount: float = Field(gt=0)
    price_currency: str = "CNY"
    price_unit: str = "per_half_day"
    max_group_size: int = Field(default=8, ge=1, le=30)
    tags: list[str] = []
    cover_image_url: Optional[str] = None


class UpdateListing(BaseModel):
    title: Optional[str] = None
    summary: Optional[str] = None
    description_md: Optional[str] = None
    city: Optional[str] = None
    languages: Optional[list[str]] = None
    price_amount: Optional[float] = None
    price_currency: Optional[str] = None
    price_unit: Optional[str] = None
    max_group_size: Optional[int] = None
    tags: Optional[list[str]] = None
    cover_image_url: Optional[str] = None
    status: Optional[str] = None  # draft, published, paused


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_listing(guide_user_id: str, req: CreateListing, db: AsyncSession = Depends(get_db)):
    """Create a new guide service listing."""
    listing = GuideListing(
        guide_user_id=guide_user_id,
        title=req.title, summary=req.summary, description_md=req.description_md,
        city=req.city, languages=req.languages,
        price_amount=req.price_amount, price_currency=req.price_currency, price_unit=req.price_unit,
        max_group_size=req.max_group_size, tags=req.tags, cover_image_url=req.cover_image_url,
        status="published",
    )
    db.add(listing)
    await db.flush()
    return {"id": listing.id, "title": listing.title, "status": listing.status, "message": "Listing created"}


@router.get("/mine")
async def list_my_listings(guide_user_id: str, db: AsyncSession = Depends(get_db)):
    """Get all listings for a guide."""
    result = await db.execute(
        select(GuideListing).where(GuideListing.guide_user_id == guide_user_id)
        .order_by(GuideListing.created_at.desc())
    )
    listings = result.scalars().all()
    return [
        {"id": l.id, "title": l.title, "summary": l.summary, "city": l.city,
         "price_amount": float(l.price_amount), "price_currency": l.price_currency,
         "price_unit": l.price_unit, "status": l.status, "cover_image_url": l.cover_image_url}
        for l in listings
    ]


@router.put("/{listing_id}")
async def update_listing(listing_id: str, guide_user_id: str, req: UpdateListing, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(GuideListing).where(GuideListing.id == listing_id, GuideListing.guide_user_id == guide_user_id)
    )
    listing = result.scalar_one_or_none()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    for field, value in req.model_dump(exclude_none=True).items():
        setattr(listing, field, value)
    await db.flush()
    return {"message": "Listing updated"}


@router.delete("/{listing_id}")
async def delete_listing(listing_id: str, guide_user_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(GuideListing).where(GuideListing.id == listing_id, GuideListing.guide_user_id == guide_user_id)
    )
    listing = result.scalar_one_or_none()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    await db.delete(listing)
    await db.flush()
    return {"message": "Listing deleted"}
