"""Discovery / matching service — surfaces guides to requesters.

Path B note: the platform suggests, the parties contract. The service ranks
by language overlap, city overlap, rating, and recency — it never decides
price, terms, or contract details.
"""
from __future__ import annotations

import uuid
from typing import Optional

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.listing import GuideListing, ListingStatus
from app.models.user import GuideProfile, KycStatus


async def search_listings(
    db: AsyncSession,
    *,
    city: Optional[str] = None,
    language: Optional[str] = None,
    party_size: Optional[int] = None,
    limit: int = 20,
    offset: int = 0,
) -> tuple[list[GuideListing], int]:
    """Return (listings, total) filtered by language/city/party_size."""
    base = (
        select(GuideListing)
        .join(GuideProfile, GuideProfile.user_id == GuideListing.guide_id)
        .where(
            GuideListing.status == ListingStatus.published,
            GuideProfile.kyc_status == KycStatus.approved,
        )
    )
    if city:
        base = base.where(GuideListing.cities.any(city))
    if language:
        base = base.where(GuideListing.languages.any(language))
    if party_size is not None:
        base = base.where(GuideListing.max_party_size >= party_size)

    total = (
        await db.execute(select(func.count()).select_from(base.subquery()))
    ).scalar_one()
    items = (
        (
            await db.execute(
                base.order_by(GuideProfile.average_rating.desc().nullslast())
                .offset(offset)
                .limit(limit)
            )
        )
        .scalars()
        .all()
    )
    return list(items), int(total)


async def get_listing(
    db: AsyncSession, listing_id: uuid.UUID
) -> Optional[GuideListing]:
    return (
        await db.execute(select(GuideListing).where(GuideListing.id == listing_id))
    ).scalar_one_or_none()
