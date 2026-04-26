"""Venue endpoints — tracks, hotels, casinos, restaurants, experiences."""

from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from api.database import get_db
from api.models import Venue
from api.schemas import VenueOut

router = APIRouter(prefix="/api/venues", tags=["venues"])


@router.get("", response_model=list[VenueOut])
async def list_venues(
    venue_type: Optional[str] = Query(None),
    region: Optional[str] = Query(None),
    city: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    q = select(Venue).options(selectinload(Venue.region))
    if venue_type:
        q = q.where(Venue.venue_type == venue_type)
    if region:
        q = q.join(Venue.region).where(Venue.region.has(name=region))
    if city:
        q = q.where(Venue.city == city)
    q = q.order_by(Venue.name).limit(200)
    result = await db.execute(q)
    return [VenueOut.model_validate(v) for v in result.scalars().all()]


@router.get("/{venue_id}", response_model=VenueOut)
async def get_venue(venue_id: int, db: AsyncSession = Depends(get_db)):
    q = select(Venue).where(Venue.id == venue_id).options(selectinload(Venue.region))
    result = await db.execute(q)
    venue = result.scalar_one_or_none()
    if not venue:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Venue not found")
    return VenueOut.model_validate(venue)
