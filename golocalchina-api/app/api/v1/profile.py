"""Profile endpoints — update tourist/guide profiles. JWT-authenticated."""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.security import get_current_user, get_current_tourist, get_current_guide
from app.models.user import User, TouristProfile, GuideProfile

router = APIRouter(prefix="/profile", tags=["profile"])


class UpdateTouristProfile(BaseModel):
    display_name: Optional[str] = None
    nationality: Optional[str] = None
    preferred_currency: Optional[str] = None


class UpdateGuideProfile(BaseModel):
    display_name: Optional[str] = None
    bio: Optional[str] = None
    languages: Optional[list[str]] = None
    service_cities: Optional[list[str]] = None
    specialties: Optional[list[str]] = None
    default_rate_cny: Optional[float] = None
    alipay_qr_url: Optional[str] = None
    wechat_pay_qr_url: Optional[str] = None
    accepts_cash: Optional[bool] = None
    payment_note: Optional[str] = None


@router.get("/me")
async def get_my_profile(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get current user's profile from JWT token."""
    user_id = current_user["user_id"]
    user_result = await db.execute(select(User).where(User.id == user_id))
    user = user_result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    profile_data = {"id": user.id, "email": user.email, "role": user.role, "locale": user.locale}

    if user.role == "tourist":
        tp = await db.execute(select(TouristProfile).where(TouristProfile.user_id == user_id))
        tp = tp.scalar_one_or_none()
        if tp:
            profile_data.update({"display_name": tp.display_name, "nationality": tp.nationality,
                                 "preferred_currency": tp.preferred_currency})
    elif user.role == "guide":
        gp = await db.execute(select(GuideProfile).where(GuideProfile.user_id == user_id))
        gp = gp.scalar_one_or_none()
        if gp:
            profile_data.update({
                "display_name": gp.display_name, "bio": gp.bio,
                "languages": gp.languages or [], "service_cities": gp.service_cities or [],
                "specialties": gp.specialties or [], "default_rate_cny": float(gp.default_rate_cny or 0),
                "alipay_qr_url": gp.alipay_qr_url, "wechat_pay_qr_url": gp.wechat_pay_qr_url,
                "accepts_cash": gp.accepts_cash, "payment_note": gp.payment_note,
                "rating_avg": float(gp.rating_avg or 0), "rating_count": gp.rating_count or 0,
            })
    return profile_data


@router.put("/me/tourist")
async def update_tourist_profile(
    req: UpdateTouristProfile,
    current_user: dict = Depends(get_current_tourist),
    db: AsyncSession = Depends(get_db),
):
    user_id = current_user["user_id"]
    result = await db.execute(select(TouristProfile).where(TouristProfile.user_id == user_id))
    tp = result.scalar_one_or_none()
    if not tp:
        raise HTTPException(status_code=404, detail="Tourist profile not found")
    for field, value in req.model_dump(exclude_none=True).items():
        setattr(tp, field, value)
    await db.flush()
    return {"message": "Profile updated"}


@router.put("/me/guide")
async def update_guide_profile(
    req: UpdateGuideProfile,
    current_user: dict = Depends(get_current_guide),
    db: AsyncSession = Depends(get_db),
):
    user_id = current_user["user_id"]
    result = await db.execute(select(GuideProfile).where(GuideProfile.user_id == user_id))
    gp = result.scalar_one_or_none()
    if not gp:
        raise HTTPException(status_code=404, detail="Guide profile not found")
    for field, value in req.model_dump(exclude_none=True).items():
        setattr(gp, field, value)
    await db.flush()
    return {"message": "Profile updated"}
