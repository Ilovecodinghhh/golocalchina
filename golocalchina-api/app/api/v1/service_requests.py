"""Service Request endpoints — connection requests. JWT-authenticated."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.security import get_current_user, get_current_guide
from app.models.listing import GuideListing
from app.models.booking import ServiceRequest
from app.schemas.service_request import CreateServiceRequest, ServiceRequestResponse

router = APIRouter(prefix="/service-requests", tags=["service-requests"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_service_request(
    req: CreateServiceRequest,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Tourist requests to connect with a guide. Listing is optional."""
    tourist_user_id = current_user["user_id"]
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
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    user_id = current_user["user_id"]
    role = current_user["role"]
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
         "quoted_amount": float(r.quoted_amount), "quoted_currency": r.quoted_currency,
         "status": r.status, "party_size": r.party_size, "language": r.language,
         "tourist_notes": r.tourist_notes, "created_at": r.created_at}
        for r in result.scalars().all()
    ]


@router.put("/{request_id}/accept")
async def accept_request(
    request_id: str,
    current_user: dict = Depends(get_current_guide),
    db: AsyncSession = Depends(get_db),
):
    guide_user_id = current_user["user_id"]
    result = await db.execute(select(ServiceRequest).where(ServiceRequest.id == request_id, ServiceRequest.guide_user_id == guide_user_id))
    sr = result.scalar_one_or_none()
    if not sr:
        raise HTTPException(status_code=404, detail="Request not found")
    sr.status = "accepted"
    await db.flush()
    return {"message": "Request accepted"}


@router.put("/{request_id}/decline")
async def decline_request(
    request_id: str,
    current_user: dict = Depends(get_current_guide),
    db: AsyncSession = Depends(get_db),
):
    guide_user_id = current_user["user_id"]
    result = await db.execute(select(ServiceRequest).where(ServiceRequest.id == request_id, ServiceRequest.guide_user_id == guide_user_id))
    sr = result.scalar_one_or_none()
    if not sr:
        raise HTTPException(status_code=404, detail="Request not found")
    sr.status = "cancelled_by_guide"
    await db.flush()
    return {"message": "Request declined"}
