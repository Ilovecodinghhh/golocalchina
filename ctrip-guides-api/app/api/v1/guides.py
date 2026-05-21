"""Guide search + detail endpoints with ranking algorithm."""
from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func, and_, case
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.user import GuideProfile, User, UserRole, UserStatus, KYCStatus
from app.models.listing import GuideListing, ListingStatus
from app.schemas.guide import GuideSearchParams, GuideListItem, GuideDetail, GuideSearchResponse

router = APIRouter(prefix="/guides", tags=["guides"])


@router.get("", response_model=GuideSearchResponse)
async def search_guides(
    city: Optional[str] = Query(None),
    language: Optional[str] = Query(None),
    specialty: Optional[str] = Query(None),
    min_rating: Optional[float] = Query(None, ge=0, le=5),
    max_price_cny: Optional[float] = Query(None, ge=0),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
):
    """Search guides with filters + ranking.
    
    Ranking algorithm (Path B compliant — no platform price manipulation):
      score = 0.40 * language_match
            + 0.25 * specialty_match
            + 0.20 * rating_normalized
            + 0.10 * response_rate
            + 0.05 * experience_factor
    """
    query = (
        select(GuideProfile)
        .join(User, User.id == GuideProfile.user_id)
        .where(
            User.status == UserStatus.active,
            GuideProfile.kyc_status == KYCStatus.approved,
        )
    )

    # Apply filters
    if city:
        query = query.where(GuideProfile.service_cities.contains([city]))
    if language:
        query = query.where(GuideProfile.languages.contains([language]))
    if specialty:
        query = query.where(GuideProfile.specialties.contains([specialty]))
    if min_rating:
        query = query.where(GuideProfile.rating_avg >= min_rating)
    if max_price_cny:
        query = query.where(GuideProfile.default_rate_cny <= max_price_cny)

    # Count total
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0

    # Apply ranking (simplified — full scoring in service layer)
    query = query.order_by(
        GuideProfile.rating_avg.desc(),
        GuideProfile.rating_count.desc(),
    )

    # Paginate
    offset = (page - 1) * per_page
    query = query.offset(offset).limit(per_page)

    result = await db.execute(query)
    guides = result.scalars().all()

    return GuideSearchResponse(
        guides=[GuideListItem.model_validate(g) for g in guides],
        total=total,
        page=page,
        per_page=per_page,
    )


@router.get("/{guide_id}", response_model=GuideDetail)
async def get_guide_detail(guide_id: UUID, db: AsyncSession = Depends(get_db)):
    """Get guide detail with their published listings."""
    result = await db.execute(
        select(GuideProfile)
        .join(User, User.id == GuideProfile.user_id)
        .where(GuideProfile.user_id == guide_id, User.status == UserStatus.active)
    )
    guide = result.scalar_one_or_none()
    if not guide:
        raise HTTPException(status_code=404, detail="Guide not found")

    # Get published listings (guide-authored content)
    listings_result = await db.execute(
        select(GuideListing)
        .where(GuideListing.guide_user_id == guide_id, GuideListing.status == ListingStatus.published)
    )
    listings = listings_result.scalars().all()

    guide_data = GuideDetail.model_validate(guide)
    guide_data.listings = [
        {
            "id": str(l.id), "title": l.title, "summary": l.summary,
            "city": l.city, "price_amount": float(l.price_amount),
            "price_currency": l.price_currency, "price_unit": l.price_unit,
        }
        for l in listings
    ]
    return guide_data
