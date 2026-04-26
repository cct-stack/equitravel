"""Experiences miner — bourbon tours, golf, fly fishing, private aviation."""

from __future__ import annotations

import logging

from sqlalchemy import select

from api.database import async_session
from api.models import VendorListing, Region

log = logging.getLogger("equitravel.miner.experiences")

CURATED_EXPERIENCES = [
    # Kentucky — Bourbon
    {"vendor_name": "Woodford Reserve Distillery Tour", "vendor_type": "tour", "description": "Premium bourbon distillery tour in Versailles, KY. 15 min from Keeneland.", "website": "https://www.woodfordreserve.com", "price_range": "$20-75/person", "region_name": "Kentucky", "country": "USA", "lat": 38.0640, "lng": -84.7389},
    {"vendor_name": "Maker's Mark Distillery", "vendor_type": "tour", "description": "Iconic bourbon distillery experience in Loretto, KY.", "website": "https://www.makersmark.com", "price_range": "$20-60/person", "region_name": "Kentucky", "country": "USA", "lat": 37.6781, "lng": -85.3395},
    {"vendor_name": "Buffalo Trace Distillery", "vendor_type": "tour", "description": "Free tours of America's oldest continuously operating distillery.", "website": "https://www.buffalotracedistillery.com", "price_range": "Free-$50/person", "region_name": "Kentucky", "country": "USA", "lat": 38.2101, "lng": -84.8615},
    {"vendor_name": "Wild Turkey Distillery", "vendor_type": "tour", "description": "Home of Wild Turkey and Russell's Reserve. Hilltop views of the Kentucky River.", "website": "https://www.wildturkeybourbon.com", "price_range": "$15-50/person", "region_name": "Kentucky", "country": "USA", "lat": 38.0067, "lng": -84.8405},
    # Private Aviation
    {"vendor_name": "NetJets", "vendor_type": "charter", "description": "Private jet service. Fractional ownership and jet card programs for racing circuit travel.", "website": "https://www.netjets.com", "price_range": "From $5,000/flight hour", "region_name": "Kentucky", "country": "USA", "lat": 38.1749, "lng": -85.7364},
    {"vendor_name": "Flexjet", "vendor_type": "charter", "description": "Luxury private jet travel, popular with racing owners and breeders.", "website": "https://www.flexjet.com", "price_range": "From $4,500/flight hour", "region_name": "Kentucky", "country": "USA", "lat": 38.1750, "lng": -85.7370},
    # Saratoga
    {"vendor_name": "Saratoga National Golf Club", "vendor_type": "golf", "description": "Championship 18-hole course in Saratoga Springs.", "website": "https://www.golfsaratoga.com", "price_range": "$75-175/round", "region_name": "New York", "country": "USA", "lat": 43.0427, "lng": -73.7538},
    {"vendor_name": "Battenkill River Fly Fishing", "vendor_type": "fishing", "description": "Guided fly fishing trips on Vermont's Battenkill — 45 min from Saratoga.", "price_range": "$350-500/day (guided)", "region_name": "New York", "country": "USA", "lat": 43.1000, "lng": -73.3200},
    # California
    {"vendor_name": "Torrey Pines Golf Course", "vendor_type": "golf", "description": "World-famous municipal course overlooking the Pacific. Host of the US Open.", "website": "https://www.torreypinesgolfcourse.com", "price_range": "$75-250/round", "region_name": "California", "country": "USA", "lat": 32.9005, "lng": -117.2428},
    # Dubai
    {"vendor_name": "Emirates Golf Club", "vendor_type": "golf", "description": "Premier desert golf during Dubai World Cup week. Faldo & Majlis courses.", "website": "https://www.dubaigolf.com", "price_range": "$200-400/round", "region_name": "Dubai", "country": "UAE", "lat": 25.0910, "lng": 55.1700},
    # UK
    {"vendor_name": "Wentworth Club", "vendor_type": "golf", "description": "Exclusive private golf near Ascot. Host of BMW PGA Championship.", "website": "https://www.wentworthclub.com", "price_range": "Members/guests only", "region_name": "Berkshire", "country": "UK", "lat": 51.3880, "lng": -0.5910},
]


async def scrape_experiences() -> dict:
    """Upsert curated experiences."""
    found = 0
    added = 0
    updated = 0

    async with async_session() as session:
        for exp in CURATED_EXPERIENCES:
            found += 1
            region = (await session.execute(
                select(Region).where(Region.name == exp["region_name"])
            )).scalar_one_or_none()
            if not region:
                region = Region(name=exp["region_name"], country=exp["country"])
                session.add(region)
                await session.flush()

            existing = (await session.execute(
                select(VendorListing).where(VendorListing.vendor_name == exp["vendor_name"])
            )).scalar_one_or_none()

            if existing:
                for k in ("website", "price_range", "description"):
                    if exp.get(k):
                        setattr(existing, k, exp[k])
                if exp.get("lat"):
                    existing.latitude = exp["lat"]
                    existing.longitude = exp["lng"]
                updated += 1
            else:
                listing = VendorListing(
                    vendor_name=exp["vendor_name"],
                    vendor_type=exp["vendor_type"],
                    description=exp.get("description"),
                    website=exp.get("website"),
                    price_range=exp.get("price_range"),
                    latitude=exp.get("lat"),
                    longitude=exp.get("lng"),
                    region_id=region.id,
                )
                session.add(listing)
                added += 1

        await session.commit()

    return {"found": found, "added": added, "updated": updated}
