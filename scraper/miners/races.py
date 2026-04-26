"""Race calendar miner — scrapes major worldwide race events.

Targets:
- Breeders' Cup, Kentucky Derby, Preakness, Belmont
- Royal Ascot, Cheltenham, Epsom Derby (UK)
- Dubai World Cup, Saudi Cup (Middle East)
- Melbourne Cup, Cox Plate (Australia)
- Japan Cup, Hong Kong International Races
- Plus Grade 1 stakes worldwide
"""

from __future__ import annotations

import logging
from datetime import date, timedelta

import httpx
from bs4 import BeautifulSoup
from sqlalchemy import select

from api.database import async_session
from api.models import Event, Venue, Region
from scraper.data import TRACK_COORDS, REGION_COORDS

log = logging.getLogger("equitravel.miner.races")

# Major races with known dates — fallback when scraping fails
# These get refreshed from live sources when available
MAJOR_RACES_2026 = [
    # USA
    {"name": "Kentucky Derby 152", "event_type": "race", "start_date": date(2026, 5, 2), "grade": "G1", "purse": "$5,000,000", "surface": "Dirt", "distance": "1¼ miles", "venue_name": "Churchill Downs", "region_name": "Kentucky", "country": "USA", "source_url": "https://www.kentuckyderby.com", "ticket_url": "https://www.kentuckyderby.com/tickets"},
    {"name": "Preakness Stakes 151", "event_type": "race", "start_date": date(2026, 5, 16), "grade": "G1", "purse": "$2,000,000", "surface": "Dirt", "distance": "1 3/16 miles", "venue_name": "Pimlico Race Course", "region_name": "Maryland", "country": "USA", "source_url": "https://www.preakness.com"},
    {"name": "Belmont Stakes 158", "event_type": "race", "start_date": date(2026, 6, 6), "grade": "G1", "purse": "$2,000,000", "surface": "Dirt", "distance": "1½ miles", "venue_name": "Saratoga Race Course", "region_name": "New York", "country": "USA", "source_url": "https://www.nyra.com/belmont"},
    {"name": "Breeders' Cup 2026", "event_type": "race", "start_date": date(2026, 11, 6), "end_date": date(2026, 11, 7), "grade": "G1", "purse": "$31,000,000", "surface": "Various", "distance": "Various", "venue_name": "Del Mar", "region_name": "California", "country": "USA", "source_url": "https://www.breederscup.com", "ticket_url": "https://www.breederscup.com/tickets"},
    {"name": "Pegasus World Cup 2026", "event_type": "race", "start_date": date(2026, 1, 24), "grade": "G1", "purse": "$3,000,000", "surface": "Dirt", "distance": "1⅛ miles", "venue_name": "Gulfstream Park", "region_name": "Florida", "country": "USA"},
    {"name": "Travers Stakes 2026", "event_type": "race", "start_date": date(2026, 8, 29), "grade": "G1", "purse": "$1,250,000", "surface": "Dirt", "distance": "1¼ miles", "venue_name": "Saratoga Race Course", "region_name": "New York", "country": "USA"},
    # UK / Ireland
    {"name": "Royal Ascot 2026", "event_type": "race", "start_date": date(2026, 6, 16), "end_date": date(2026, 6, 20), "grade": "G1", "purse": "£8,000,000+", "surface": "Turf", "distance": "Various", "venue_name": "Ascot Racecourse", "region_name": "Berkshire", "country": "UK", "source_url": "https://www.ascot.com", "ticket_url": "https://www.ascot.com/tickets"},
    {"name": "Cheltenham Festival 2026", "event_type": "race", "start_date": date(2026, 3, 10), "end_date": date(2026, 3, 13), "grade": "G1", "purse": "£6,000,000+", "surface": "Turf (NH)", "distance": "Various", "venue_name": "Cheltenham Racecourse", "region_name": "Gloucestershire", "country": "UK", "source_url": "https://www.thejockeyclub.co.uk/cheltenham"},
    {"name": "Epsom Derby 2026", "event_type": "race", "start_date": date(2026, 6, 6), "grade": "G1", "purse": "£1,500,000", "surface": "Turf", "distance": "1½ miles", "venue_name": "Epsom Downs", "region_name": "Surrey", "country": "UK"},
    {"name": "Goodwood Festival 2026", "event_type": "race", "start_date": date(2026, 7, 28), "end_date": date(2026, 8, 1), "grade": "G1", "surface": "Turf", "distance": "Various", "venue_name": "Goodwood Racecourse", "region_name": "West Sussex", "country": "UK"},
    # Middle East
    {"name": "Dubai World Cup 2026", "event_type": "race", "start_date": date(2026, 3, 28), "grade": "G1", "purse": "$12,000,000", "surface": "Dirt", "distance": "2000m", "venue_name": "Meydan Racecourse", "region_name": "Dubai", "country": "UAE", "source_url": "https://www.dubairacingclub.com", "ticket_url": "https://www.dubairacingclub.com/tickets"},
    {"name": "Saudi Cup 2026", "event_type": "race", "start_date": date(2026, 2, 21), "grade": "G1", "purse": "$20,000,000", "surface": "Dirt", "distance": "1800m", "venue_name": "King Abdulaziz Racecourse", "region_name": "Riyadh", "country": "Saudi Arabia", "source_url": "https://thesaudicup.com"},
    # Australia
    {"name": "Melbourne Cup 2026", "event_type": "race", "start_date": date(2026, 11, 3), "grade": "G1", "purse": "A$8,000,000", "surface": "Turf", "distance": "3200m", "venue_name": "Flemington Racecourse", "region_name": "Victoria", "country": "Australia", "source_url": "https://www.flemington.com.au"},
    {"name": "Cox Plate 2026", "event_type": "race", "start_date": date(2026, 10, 24), "grade": "G1", "purse": "A$5,000,000", "surface": "Turf", "distance": "2040m", "venue_name": "Moonee Valley Racecourse", "region_name": "Victoria", "country": "Australia"},
    {"name": "The Everest 2026", "event_type": "race", "start_date": date(2026, 10, 17), "grade": "G1", "purse": "A$20,000,000", "surface": "Turf", "distance": "1200m", "venue_name": "Royal Randwick", "region_name": "New South Wales", "country": "Australia"},
    # Japan
    {"name": "Japan Cup 2026", "event_type": "race", "start_date": date(2026, 11, 29), "grade": "G1", "purse": "¥600,000,000", "surface": "Turf", "distance": "2400m", "venue_name": "Tokyo Racecourse", "region_name": "Tokyo", "country": "Japan"},
    # Hong Kong
    {"name": "Hong Kong International Races 2026", "event_type": "race", "start_date": date(2026, 12, 13), "grade": "G1", "purse": "HK$100,000,000+", "surface": "Turf", "distance": "Various", "venue_name": "Sha Tin Racecourse", "region_name": "Hong Kong", "country": "Hong Kong", "source_url": "https://www.hkjc.com"},
    # France
    {"name": "Prix de l'Arc de Triomphe 2026", "event_type": "race", "start_date": date(2026, 10, 4), "grade": "G1", "purse": "€5,000,000", "surface": "Turf", "distance": "2400m", "venue_name": "ParisLongchamp", "region_name": "Paris", "country": "France", "source_url": "https://www.france-galop.com"},
]


async def scrape_races() -> dict:
    """Scrape race calendars and upsert into DB."""
    found = 0
    added = 0
    updated = 0

    async with async_session() as session:
        for race_data in MAJOR_RACES_2026:
            found += 1
            # Ensure region exists
            region = (await session.execute(
                select(Region).where(Region.name == race_data["region_name"])
            )).scalar_one_or_none()
            if not region:
                rlat, rlng = REGION_COORDS.get(race_data["region_name"], (None, None))
                region = Region(
                    name=race_data["region_name"],
                    country=race_data["country"],
                    latitude=rlat,
                    longitude=rlng,
                )
                session.add(region)
                await session.flush()
            elif region.latitude is None:
                rlat, rlng = REGION_COORDS.get(race_data["region_name"], (None, None))
                if rlat:
                    region.latitude = rlat
                    region.longitude = rlng

            # Ensure venue exists
            venue = (await session.execute(
                select(Venue).where(Venue.name == race_data["venue_name"])
            )).scalar_one_or_none()
            vlat, vlng = TRACK_COORDS.get(race_data["venue_name"], (None, None))
            if not venue:
                venue = Venue(
                    name=race_data["venue_name"],
                    venue_type="track",
                    region_id=region.id,
                    latitude=vlat,
                    longitude=vlng,
                )
                session.add(venue)
                await session.flush()
            elif venue.latitude is None and vlat:
                venue.latitude = vlat
                venue.longitude = vlng

            # Upsert event
            existing = (await session.execute(
                select(Event).where(
                    Event.name == race_data["name"],
                    Event.start_date == race_data["start_date"],
                )
            )).scalar_one_or_none()

            if existing:
                for key in ("purse", "grade", "surface", "distance", "ticket_url", "source_url"):
                    if key in race_data and race_data[key]:
                        setattr(existing, key, race_data[key])
                updated += 1
            else:
                event = Event(
                    name=race_data["name"],
                    event_type=race_data["event_type"],
                    start_date=race_data["start_date"],
                    end_date=race_data.get("end_date"),
                    purse=race_data.get("purse"),
                    grade=race_data.get("grade"),
                    surface=race_data.get("surface"),
                    distance=race_data.get("distance"),
                    ticket_url=race_data.get("ticket_url"),
                    source_url=race_data.get("source_url"),
                    venue_id=venue.id,
                    region_id=region.id,
                )
                session.add(event)
                added += 1

        await session.commit()

    # TODO: Live scraping from breederscup.com, kentuckyderby.com, etc.
    # Will add httpx + BeautifulSoup scraping in next iteration

    return {"found": found, "added": added, "updated": updated}
