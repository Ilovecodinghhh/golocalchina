"""Service Request endpoints — connection requests only, no payment processing."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.listing import GuideListing
from app.models.booking import ServiceRequest
from app.schemas.service_request import CreateServiceRequest, ServiceRequestResponse

router = APIRouter(prefix="/service-requests", tags=["service-requests"])


@router.post("", response_model=ServiceRequestResponse, status_code=status.HTTP_201_CREATED)
async def create_service_request(req: CreateServiceRequest, db: AsyncSession = Depends(get_db)):
    listing_result = await db.execute(
        select(GuideListing).where(GuideListing.id == str(req.listing_id), GuideListing.status == "published")
    )
    listing = listing_result.scalar_one_or_none()
    if not listing:
        raise HTTPException(status_code=404, detail="Guide service listing not found")

    sr = ServiceRequest(
        tourist_user_id="00000000-0000-0000-0000-000000000001",  # TODO: from JWT
        guide_user_id=listing.guide_user_id,
        listing_id=listing.id,
        service_date=str(req.service_date),
        party_size=req.party_size,
        language=req.language,
        tourist_notes=req.tourist_notes,
        quoted_amount=float(listing.price_amount),
        quoted_currency=listing.price_currency,
        status="pending",
    )
    db.add(sr)
    await db.flush()
    return ServiceRequestResponse.model_validate(sr)


@router.get("/mine", response_model=list[ServiceRequestResponse])
async def list_my_requests(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ServiceRequest).order_by(ServiceRequest.created_at.desc()).limit(50))
    return [ServiceRequestResponse.model_validate(r) for r in result.scalars().all()]
