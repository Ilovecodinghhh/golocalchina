"""Public explore endpoint — search published listings with guide info.
This is what tourists see when browsing."""
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.models.listing import GuideListing
from app.models.user import GuideProfile, User

router = APIRouter(prefix="/explore", tags=["explore"])


@router.get("/listings")
async def search_listings(
    city: Optional[str] = Query(None),
    language: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
):
    """Search published guide listings. No auth required."""
    query = (
        select(GuideListing, GuideProfile)
        .join(GuideProfile, GuideProfile.user_id == GuideListing.guide_user_id)
        .where(GuideListing.status == "published")
    )

    if city:
        query = query.where(GuideListing.city == city)
    if language:
        query = query.where(GuideListing.languages.contains(language))

    # Count
    count_q = select(func.count()).select_from(
        select(GuideListing).where(GuideListing.status == "published").subquery()
    )
    if city:
        count_q = select(func.count()).select_from(
            select(GuideListing).where(GuideListing.status == "published", GuideListing.city == city).subquery()
        )
    total_result = await db.execute(count_q)
    total = total_result.scalar() or 0

    query = query.offset((page - 1) * per_page).limit(per_page)
    result = await db.execute(query)
    rows = result.all()

    listings = []
    for listing, guide in rows:
        listings.append({
            "id": listing.id,
            "title": listing.title,
            "summary": listing.summary,
            "city": listing.city,
            "price_amount": float(listing.price_amount),
            "price_currency": listing.price_currency,
            "price_unit": listing.price_unit,
            "cover_image_url": listing.cover_image_url,
            "languages": listing.languages or [],
            "tags": listing.tags or [],
            "guide": {
                "user_id": guide.user_id,
                "display_name": guide.display_name,
                "bio": guide.bio,
                "languages": guide.languages or [],
                "service_cities": guide.service_cities or [],
                "specialties": guide.specialties or [],
                "rating_avg": float(guide.rating_avg or 0),
                "rating_count": guide.rating_count or 0,
                "default_rate_cny": float(guide.default_rate_cny or 0),
                "avatar_url": guide.avatar_url,
                "is_certified": guide.guide_license_no is not None and guide.guide_license_no != "",
                "accepts_cash": guide.accepts_cash,
                "payment_note": guide.payment_note,
            },
        })

    return {"listings": listings, "total": total, "page": page, "per_page": per_page}
