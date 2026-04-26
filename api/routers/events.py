"""Event endpoints — list, filter, detail."""

from __future__ import annotations

import datetime as dt
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from api.database import get_db
from api.models import Event, VendorListing, TicketPrice, HotelRate, TripEstimate
from api.schemas import EventOut, EventListResponse, EventDetailResponse, TicketPriceOut, VendorOut, HotelRateOut, TripEstimateOut

router = APIRouter(prefix="/api/events", tags=["events"])


@router.get("", response_model=EventListResponse)
async def list_events(
    event_type: Optional[str] = Query(None, description="Filter by type: race, auction, festival, experience"),
    region: Optional[str] = Query(None, description="Filter by region name"),
    country: Optional[str] = Query(None, description="Filter by country"),
    from_date: Optional[dt.date] = Query(None, description="Events starting on or after this date"),
    to_date: Optional[dt.date] = Query(None, description="Events starting on or before this date"),
    grade: Optional[str] = Query(None, description="Race grade filter: G1, G2, G3"),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
):
    """Return a paginated, filterable list of upcoming events."""
    q = select(Event).options(selectinload(Event.venue), selectinload(Event.region))

    if event_type:
        q = q.where(Event.event_type == event_type)
    if region:
        q = q.join(Event.region).where(Event.region.has(name=region))
    if country:
        q = q.join(Event.region).where(Event.region.has(country=country))
    if from_date:
        q = q.where(Event.start_date >= from_date)
    else:
        q = q.where(Event.start_date >= dt.date.today())
    if to_date:
        q = q.where(Event.start_date <= to_date)
    if grade:
        q = q.where(Event.grade == grade)

    # Count
    count_q = select(func.count()).select_from(q.subquery())
    total = (await db.execute(count_q)).scalar() or 0

    # Paginate
    q = q.order_by(Event.start_date.asc()).offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(q)
    events = result.scalars().all()

    return EventListResponse(
        events=[EventOut.model_validate(e) for e in events],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/{event_id}", response_model=EventDetailResponse)
async def get_event(event_id: int, db: AsyncSession = Depends(get_db)):
    """Return a single event with all associated services and pricing."""
    from fastapi import HTTPException

    q = select(Event).where(Event.id == event_id).options(
        selectinload(Event.venue),
        selectinload(Event.region),
        selectinload(Event.ticket_prices),
    )
    result = await db.execute(q)
    event = result.scalar_one_or_none()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    event_out = EventOut.model_validate(event)
    ticket_prices = [TicketPriceOut.model_validate(tp) for tp in event.ticket_prices]

    # Find all vendors in the same region
    nearby_hotels: list[VendorOut] = []
    nearby_casinos: list[VendorOut] = []
    nearby_restaurants: list[VendorOut] = []
    nearby_experiences: list[VendorOut] = []
    hotel_rates: list[HotelRateOut] = []

    if event.region_id:
        vendors_q = select(VendorListing).where(VendorListing.region_id == event.region_id)
        vendors_result = await db.execute(vendors_q)
        vendors = vendors_result.scalars().all()

        for v in vendors:
            vo = VendorOut.model_validate(v)
            if v.vendor_type == "hotel":
                nearby_hotels.append(vo)
            elif v.vendor_type == "casino":
                nearby_casinos.append(vo)
            elif v.vendor_type == "restaurant":
                nearby_restaurants.append(vo)
            else:
                nearby_experiences.append(vo)

        # Get hotel rates for this event
        rates_q = select(HotelRate).where(HotelRate.event_id == event_id)
        rates_result = await db.execute(rates_q)
        for rate in rates_result.scalars().all():
            hotel_rates.append(HotelRateOut(
                id=rate.id,
                vendor_name=rate.vendor.vendor_name if rate.vendor else "Unknown",
                vendor_type=rate.vendor.vendor_type if rate.vendor else "hotel",
                check_in=rate.check_in,
                check_out=rate.check_out,
                room_type=rate.room_type,
                rate_per_night=rate.rate_per_night,
                currency=rate.currency,
                source=rate.source,
                url=rate.url,
                available=rate.available,
                scraped_at=rate.scraped_at,
            ))

    # Trip estimate
    trip_out = None
    trip_q = select(TripEstimate).where(TripEstimate.event_id == event_id)
    trip_result = await db.execute(trip_q)
    trip = trip_result.scalar_one_or_none()
    if trip:
        trip_out = TripEstimateOut.model_validate(trip)

    return EventDetailResponse(
        event=event_out,
        ticket_prices=ticket_prices,
        nearby_hotels=nearby_hotels,
        nearby_casinos=nearby_casinos,
        nearby_restaurants=nearby_restaurants,
        nearby_experiences=nearby_experiences,
        hotel_rates=hotel_rates,
        trip_estimate=trip_out,
    )
