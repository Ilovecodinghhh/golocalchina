"""Service Request endpoints — tourist requests to connect with a guide.
Path B: This is a CONNECTION REQUEST, not a tour booking."""
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.config import settings
from app.models.user import User, GuideProfile
from app.models.listing import GuideListing, ListingStatus
from app.models.booking import ServiceRequest, RequestStatus
from app.schemas.service_request import CreateServiceRequest, ServiceRequestResponse

router = APIRouter(prefix="/service-requests", tags=["service-requests"])


@router.post("", response_model=ServiceRequestResponse, status_code=status.HTTP_201_CREATED)
async def create_service_request(
    req: CreateServiceRequest,
    db: AsyncSession = Depends(get_db),
    # TODO: Add JWT auth dependency — current_user: User = Depends(get_current_tourist)
):
    """Tourist requests to connect with a guide via a listing.
    
    Flow:
    1. Tourist submits request → status: pending
    2. Guide accepts/declines (guide's choice, NOT platform's)
    3. If accepted → tourist pays via PSP (Airwallex)
    4. Service happens
    5. Both parties review
    
    Platform role: facilitate the connection. We do NOT organize the service.
    """
    # Fetch listing (guide-authored content)
    listing_result = await db.execute(
        select(GuideListing).where(
            GuideListing.id == req.listing_id,
            GuideListing.status == ListingStatus.published,
        )
    )
    listing = listing_result.scalar_one_or_none()
    if not listing:
        raise HTTPException(status_code=404, detail="Guide service listing not found")

    # Calculate fees — 信息服务费 (Information Service Fee)
    quoted_amount = float(listing.price_amount)
    fee_pct = settings.platform_fee_pct
    platform_fee = round(quoted_amount * fee_pct / 100, 2)
    guide_payout = round(quoted_amount - platform_fee, 2)

    service_request = ServiceRequest(
        tourist_user_id=UUID("00000000-0000-0000-0000-000000000001"),  # TODO: from JWT
        guide_user_id=listing.guide_user_id,
        listing_id=listing.id,
        service_date=req.service_date,
        party_size=req.party_size,
        language=req.language,
        tourist_notes=req.tourist_notes,
        quoted_amount=quoted_amount,
        quoted_currency=listing.price_currency,
        platform_fee_pct=fee_pct,
        platform_fee_amount=platform_fee,
        guide_payout_amount=guide_payout,
        status=RequestStatus.pending,
    )
    db.add(service_request)
    await db.flush()

    return ServiceRequestResponse.model_validate(service_request)


@router.get("/mine", response_model=list[ServiceRequestResponse])
async def list_my_requests(
    db: AsyncSession = Depends(get_db),
    # TODO: current_user: User = Depends(get_current_user)
):
    """List service requests for the current user (tourist or guide)."""
    # TODO: Filter by current user from JWT
    result = await db.execute(
        select(ServiceRequest).order_by(ServiceRequest.created_at.desc()).limit(50)
    )
    requests = result.scalars().all()
    return [ServiceRequestResponse.model_validate(r) for r in requests]
