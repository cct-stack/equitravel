"""Auction miner — horse sales at Keeneland, Fasig-Tipton, Tattersalls, Goffs, Magic Millions."""

from __future__ import annotations

import logging
from datetime import date

from sqlalchemy import select

from api.database import async_session
from api.models import Event, Venue, Region

log = logging.getLogger("equitravel.miner.auctions")

MAJOR_AUCTIONS_2026 = [
    # Keeneland (Lexington, KY)
    {"name": "Keeneland January Horses of All Ages Sale", "start_date": date(2026, 1, 12), "end_date": date(2026, 1, 15), "venue_name": "Keeneland", "region_name": "Kentucky", "country": "USA", "source_url": "https://www.keeneland.com/sales"},
    {"name": "Keeneland April Sale of Two-Year-Olds in Training", "start_date": date(2026, 4, 7), "end_date": date(2026, 4, 8), "venue_name": "Keeneland", "region_name": "Kentucky", "country": "USA"},
    {"name": "Keeneland September Yearling Sale", "start_date": date(2026, 9, 7), "end_date": date(2026, 9, 19), "venue_name": "Keeneland", "region_name": "Kentucky", "country": "USA", "source_url": "https://www.keeneland.com/sales"},
    {"name": "Keeneland November Breeding Stock Sale", "start_date": date(2026, 11, 2), "end_date": date(2026, 11, 14), "venue_name": "Keeneland", "region_name": "Kentucky", "country": "USA"},
    # Fasig-Tipton
    {"name": "Fasig-Tipton Kentucky Winter Mixed", "start_date": date(2026, 2, 9), "end_date": date(2026, 2, 10), "venue_name": "Fasig-Tipton", "region_name": "Kentucky", "country": "USA", "source_url": "https://www.fasigtipton.com"},
    {"name": "Fasig-Tipton Saratoga Selected Yearlings", "start_date": date(2026, 8, 10), "end_date": date(2026, 8, 11), "venue_name": "Fasig-Tipton Saratoga", "region_name": "New York", "country": "USA"},
    {"name": "Fasig-Tipton November Sale", "start_date": date(2026, 11, 8), "end_date": date(2026, 11, 10), "venue_name": "Fasig-Tipton", "region_name": "Kentucky", "country": "USA"},
    # Tattersalls (UK)
    {"name": "Tattersalls Craven Breeze-Up Sale", "start_date": date(2026, 4, 15), "end_date": date(2026, 4, 16), "venue_name": "Tattersalls", "region_name": "Newmarket", "country": "UK", "source_url": "https://www.tattersalls.com"},
    {"name": "Tattersalls October Yearling Sale", "start_date": date(2026, 10, 5), "end_date": date(2026, 10, 15), "venue_name": "Tattersalls", "region_name": "Newmarket", "country": "UK"},
    {"name": "Tattersalls December Mare Sale", "start_date": date(2026, 11, 30), "end_date": date(2026, 12, 4), "venue_name": "Tattersalls", "region_name": "Newmarket", "country": "UK"},
    # Goffs (Ireland)
    {"name": "Goffs Orby Sale", "start_date": date(2026, 9, 29), "end_date": date(2026, 9, 30), "venue_name": "Goffs", "region_name": "County Kildare", "country": "Ireland", "source_url": "https://www.goffs.com"},
    {"name": "Goffs November Foal Sale", "start_date": date(2026, 11, 10), "end_date": date(2026, 11, 14), "venue_name": "Goffs", "region_name": "County Kildare", "country": "Ireland"},
    # Magic Millions (Australia)
    {"name": "Magic Millions Gold Coast Yearling Sale", "start_date": date(2026, 1, 7), "end_date": date(2026, 1, 14), "venue_name": "Magic Millions Sales Complex", "region_name": "Queensland", "country": "Australia", "source_url": "https://www.magicmillions.com.au"},
    # Arqana (France)
    {"name": "Arqana August Yearling Sale", "start_date": date(2026, 8, 15), "end_date": date(2026, 8, 17), "venue_name": "Arqana", "region_name": "Deauville", "country": "France", "source_url": "https://www.arqana.com"},
]


async def scrape_auctions() -> dict:
    """Upsert auction events into DB."""
    found = 0
    added = 0
    updated = 0

    async with async_session() as session:
        for auction_data in MAJOR_AUCTIONS_2026:
            found += 1
            region = (await session.execute(
                select(Region).where(Region.name == auction_data["region_name"])
            )).scalar_one_or_none()
            if not region:
                region = Region(name=auction_data["region_name"], country=auction_data["country"])
                session.add(region)
                await session.flush()

            venue = (await session.execute(
                select(Venue).where(Venue.name == auction_data["venue_name"])
            )).scalar_one_or_none()
            if not venue:
                venue = Venue(name=auction_data["venue_name"], venue_type="auction_house", region_id=region.id)
                session.add(venue)
                await session.flush()

            existing = (await session.execute(
                select(Event).where(Event.name == auction_data["name"], Event.start_date == auction_data["start_date"])
            )).scalar_one_or_none()

            if existing:
                updated += 1
            else:
                event = Event(
                    name=auction_data["name"],
                    event_type="auction",
                    start_date=auction_data["start_date"],
                    end_date=auction_data.get("end_date"),
                    source_url=auction_data.get("source_url"),
                    venue_id=venue.id,
                    region_id=region.id,
                )
                session.add(event)
                added += 1

        await session.commit()

    return {"found": found, "added": added, "updated": updated}
