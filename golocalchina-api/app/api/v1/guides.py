"""Guide search + detail endpoints."""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.user import GuideProfile, User
from app.models.listing import GuideListing
from app.schemas.guide import GuideListItem, GuideDetail, GuideSearchResponse

router = APIRouter(prefix="/guides", tags=["guides"])


@router.get("", response_model=GuideSearchResponse)
async def search_guides(
    city: Optional[str] = Query(None),
    language: Optional[str] = Query(None),
    specialty: Optional[str] = Query(None),
    min_rating: Optional[float] = Query(None, ge=0, le=5),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
):
    query = (
        select(GuideProfile)
        .join(User, User.id == GuideProfile.user_id)
        .where(User.status == "active", GuideProfile.kyc_status == "approved")
    )

    if city:
        query = query.where(GuideProfile.service_cities.contains(city))
    if language:
        query = query.where(GuideProfile.languages.contains(language))
    if specialty:
        query = query.where(GuideProfile.specialties.contains(specialty))
    if min_rating:
        query = query.where(GuideProfile.rating_avg >= min_rating)

    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0

    query = query.order_by(GuideProfile.rating_avg.desc()).offset((page - 1) * per_page).limit(per_page)
    result = await db.execute(query)
    guides = result.scalars().all()

    return GuideSearchResponse(
        guides=[GuideListItem.model_validate(g) for g in guides],
        total=total, page=page, per_page=per_page,
    )


@router.get("/{guide_id}")
async def get_guide_detail(guide_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(GuideProfile).join(User, User.id == GuideProfile.user_id)
        .where(GuideProfile.user_id == guide_id, User.status == "active")
    )
    guide = result.scalar_one_or_none()
    if not guide:
        raise HTTPException(status_code=404, detail="Guide not found")

    listings_result = await db.execute(
        select(GuideListing).where(GuideListing.guide_user_id == guide_id, GuideListing.status == "published")
    )
    listings = listings_result.scalars().all()

    return {
        **GuideListItem.model_validate(guide).model_dump(),
        "guide_license_no": guide.guide_license_no,
        "guide_license_issuer": guide.guide_license_issuer,
        "kyc_status": guide.kyc_status,
        "accepts_cash": guide.accepts_cash,
        "alipay_qr_url": guide.alipay_qr_url,
        "wechat_pay_qr_url": guide.wechat_pay_qr_url,
        "payment_note": guide.payment_note,
        "listings": [
            {"id": l.id, "title": l.title, "summary": l.summary, "city": l.city,
             "price_amount": float(l.price_amount), "price_currency": l.price_currency, "price_unit": l.price_unit}
            for l in listings
        ],
    }
