"""Service Request endpoints — connection requests."""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.models.listing import GuideListing
from app.models.booking import ServiceRequest
from app.schemas.service_request import CreateServiceRequest, ServiceRequestResponse

router = APIRouter(prefix="/service-requests", tags=["service-requests"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_service_request(
    req: CreateServiceRequest,
    tourist_user_id: str = Query(...),
    db: AsyncSession = Depends(get_db),
):
    """Tourist requests to connect with a guide. Listing is optional."""
    quoted = req.quoted_amount or 0
    currency = req.quoted_currency or "CNY"

    # If listing provided, get price from it
    if req.listing_id:
        listing_result = await db.execute(
            select(GuideListing).where(GuideListing.id == req.listing_id)
        )
        listing = listing_result.scalar_one_or_none()
        if listing:
            quoted = float(listing.price_amount)
            currency = listing.price_currency

    sr = ServiceRequest(
        tourist_user_id=tourist_user_id,
        guide_user_id=req.guide_user_id,
        listing_id=req.listing_id,
        service_date=str(req.service_date),
        service_time_hour=req.service_time_hour,
        party_size=req.party_size,
        language=req.language,
        tourist_notes=req.tourist_notes,
        quoted_amount=quoted,
        quoted_currency=currency,
        status="pending",
    )
    db.add(sr)
    await db.flush()
    return {
        "id": sr.id, "tourist_user_id": sr.tourist_user_id, "guide_user_id": sr.guide_user_id,
        "listing_id": sr.listing_id, "service_date": sr.service_date,
        "quoted_amount": float(sr.quoted_amount), "quoted_currency": sr.quoted_currency,
        "status": sr.status, "message": "Connection request sent!"
    }


@router.get("/mine")
async def list_my_requests(
    user_id: str = Query(...), role: str = Query("tourist"),
    db: AsyncSession = Depends(get_db),
):
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
    return [
        {"id": r.id, "tourist_user_id": r.tourist_user_id, "guide_user_id": r.guide_user_id,
         "listing_id": r.listing_id, "service_date": r.service_date,
         "service_time_hour": r.service_time_hour,
         "quoted_amount": float(r.quoted_amount), "quoted_currency": r.quoted_currency,
         "status": r.status, "party_size": r.party_size, "language": r.language,
         "tourist_notes": r.tourist_notes, "created_at": r.created_at}
        for r in result.scalars().all()
    ]


@router.put("/{request_id}/accept")
async def accept_request(request_id: str, guide_user_id: str = Query(...), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ServiceRequest).where(ServiceRequest.id == request_id, ServiceRequest.guide_user_id == guide_user_id))
    sr = result.scalar_one_or_none()
    if not sr: raise HTTPException(status_code=404, detail="Request not found")
    sr.status = "accepted"
    await db.flush()
    return {"message": "Request accepted"}


@router.put("/{request_id}/decline")
async def decline_request(request_id: str, guide_user_id: str = Query(...), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ServiceRequest).where(ServiceRequest.id == request_id, ServiceRequest.guide_user_id == guide_user_id))
    sr = result.scalar_one_or_none()
    if not sr: raise HTTPException(status_code=404, detail="Request not found")
    sr.status = "cancelled_by_guide"
    await db.flush()
    return {"message": "Request declined"}


@router.put("/{request_id}/met")
async def mark_as_met(request_id: str, guide_user_id: str = Query(...), db: AsyncSession = Depends(get_db)):
    """Guide marks that they have met the tourist. This enables the tourist to write a review."""
    result = await db.execute(
        select(ServiceRequest).where(
            ServiceRequest.id == request_id,
            ServiceRequest.guide_user_id == guide_user_id
        )
    )
    sr = result.scalar_one_or_none()
    if not sr:
        raise HTTPException(status_code=404, detail="Request not found")
    if sr.status not in ("accepted",):
        raise HTTPException(status_code=400, detail="Can only mark accepted requests as met")
    sr.status = "met"
    await db.flush()
    return {"message": "Service marked as met. Tourist can now write a review."}
