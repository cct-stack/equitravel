"""Hotel, casino & restaurant miner — lodging, gaming, and dining near major tracks."""

from __future__ import annotations

import logging

from sqlalchemy import select

from api.database import async_session
from api.models import Venue, VendorListing, Region
from scraper.data import HOTELS, CASINOS, RESTAURANTS

log = logging.getLogger("equitravel.miner.hotels")

ALL_VENDORS = HOTELS + CASINOS + RESTAURANTS


async def _upsert_vendors(vendor_list: list[dict]) -> dict:
    """Generic upsert for vendor listings with coordinates."""
    found = 0
    added = 0
    updated = 0

    async with async_session() as session:
        for item in vendor_list:
            found += 1
            region = (await session.execute(
                select(Region).where(Region.name == item["region_name"])
            )).scalar_one_or_none()
            if not region:
                region = Region(name=item["region_name"], country=item["country"])
                session.add(region)
                await session.flush()

            existing = (await session.execute(
                select(VendorListing).where(VendorListing.vendor_name == item["vendor_name"])
            )).scalar_one_or_none()

            if existing:
                for k in ("website", "price_range", "description", "latitude", "longitude"):
                    val = item.get({"latitude": "lat", "longitude": "lng"}.get(k, k))
                    if val is not None:
                        setattr(existing, k, val)
                updated += 1
            else:
                listing = VendorListing(
                    vendor_name=item["vendor_name"],
                    vendor_type=item["vendor_type"],
                    description=item.get("description"),
                    website=item.get("website"),
                    price_range=item.get("price_range"),
                    latitude=item.get("lat"),
                    longitude=item.get("lng"),
                    region_id=region.id,
                )
                session.add(listing)
                added += 1

        await session.commit()

    return {"found": found, "added": added, "updated": updated}


async def scrape_hotels() -> dict:
    """Upsert all hotels, casinos, and restaurants."""
    return await _upsert_vendors(ALL_VENDORS)
