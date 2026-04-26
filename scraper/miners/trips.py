"""Trip cost estimator — calculates suggested 3-5 day trip budgets per event."""

from __future__ import annotations

import logging

from sqlalchemy import select, delete

from api.database import async_session
from api.models import Event, TripEstimate
from scraper.data import TRIP_ESTIMATES

log = logging.getLogger("equitravel.miner.trips")


async def scrape_trips() -> dict:
    """Generate trip cost estimates for all events with pricing data."""
    found = 0
    added = 0

    async with async_session() as session:
        events = (await session.execute(
            select(Event).where(Event.event_type == "race")
        )).scalars().all()

        for event in events:
            # Match event name to trip data
            estimate = None
            for key, data in TRIP_ESTIMATES.items():
                if key.lower() in event.name.lower():
                    estimate = data
                    break

            if not estimate:
                continue

            found += 1

            # Clear old estimates for this event
            await session.execute(
                delete(TripEstimate).where(TripEstimate.event_id == event.id)
            )

            nights = estimate["nights"]
            currency = estimate["currency"]
            hotel_low = estimate["hotel_low"]
            hotel_high = estimate["hotel_high"]
            tickets_low = estimate["tickets_low"]
            tickets_high = estimate["tickets_high"]
            dining_per_day = estimate["dining_per_day"]
            exp_per_day = estimate["experiences_per_day"]
            transport = estimate["transport"]

            total_low = (hotel_low * nights) + tickets_low + (dining_per_day * nights) + (exp_per_day * nights) + transport
            total_high = (hotel_high * nights) + tickets_high + (dining_per_day * nights) + (exp_per_day * nights) + transport

            te = TripEstimate(
                event_id=event.id,
                nights=nights,
                currency=currency,
                hotel_low=hotel_low,
                hotel_high=hotel_high,
                tickets_low=tickets_low,
                tickets_high=tickets_high,
                dining_per_day=dining_per_day,
                experiences_per_day=exp_per_day,
                transport=transport,
                total_low=round(total_low),
                total_high=round(total_high),
            )
            session.add(te)
            added += 1

        await session.commit()

    return {"found": found, "added": added, "updated": 0}
