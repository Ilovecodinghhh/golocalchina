"""Service Request endpoints — connection requests only."""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.models.listing import GuideListing
from app.models.booking import ServiceRequest
from app.schemas.service_request import CreateServiceRequest, ServiceRequestResponse

router = APIRouter(prefix="/service-requests", tags=["service-requests"])


@router.post("", response_model=ServiceRequestResponse, status_code=status.HTTP_201_CREATED)
async def create_service_request(
    req: CreateServiceRequest,
    tourist_user_id: str = Query(..., description="Tourist's user ID"),
    db: AsyncSession = Depends(get_db),
):
    """Tourist requests to connect with a guide."""
    listing_result = await db.execute(
        select(GuideListing).where(GuideListing.id == str(req.listing_id), GuideListing.status == "published")
    )
    listing = listing_result.scalar_one_or_none()
    if not listing:
        raise HTTPException(status_code=404, detail="Guide service listing not found")

    sr = ServiceRequest(
        tourist_user_id=tourist_user_id,
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


@router.get("/mine")
async def list_my_requests(
    user_id: str = Query(..., description="User ID"),
    role: str = Query("tourist", description="User role"),
    db: AsyncSession = Depends(get_db),
):
    """List service requests for a user (as tourist or guide)."""
    if role == "guide":
        result = await db.execute(
            select(ServiceRequest).where(ServiceRequest.guide_user_id == user_id)
            .order_by(ServiceRequest.created_at.desc()).limit(50)
        )
    else:
        result = await db.execute(
            select(ServiceRequest).where(ServiceRequest.tourist_user_id == user_id)
            .order_by(ServiceRequest.created_at.desc()).limit(50)
        )
    requests = result.scalars().all()
    return [
        {
            "id": r.id, "tourist_user_id": r.tourist_user_id, "guide_user_id": r.guide_user_id,
            "listing_id": r.listing_id, "service_date": r.service_date,
            "quoted_amount": float(r.quoted_amount), "quoted_currency": r.quoted_currency,
            "status": r.status, "party_size": r.party_size, "language": r.language,
            "tourist_notes": r.tourist_notes, "created_at": r.created_at,
        }
        for r in requests
    ]


@router.put("/{request_id}/accept")
async def accept_request(request_id: str, guide_user_id: str = Query(...), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(ServiceRequest).where(ServiceRequest.id == request_id, ServiceRequest.guide_user_id == guide_user_id)
    )
    sr = result.scalar_one_or_none()
    if not sr:
        raise HTTPException(status_code=404, detail="Request not found")
    sr.status = "accepted"
    await db.flush()
    return {"message": "Request accepted", "status": "accepted"}


@router.put("/{request_id}/decline")
async def decline_request(request_id: str, guide_user_id: str = Query(...), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(ServiceRequest).where(ServiceRequest.id == request_id, ServiceRequest.guide_user_id == guide_user_id)
    )
    sr = result.scalar_one_or_none()
    if not sr:
        raise HTTPException(status_code=404, detail="Request not found")
    sr.status = "cancelled_by_guide"
    await db.flush()
    return {"message": "Request declined"}
