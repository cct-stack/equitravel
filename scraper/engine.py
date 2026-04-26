"""Scraping engine — orchestrates all miners."""

from __future__ import annotations

import logging
import time

from api.database import async_session
from api.models import ScrapeLog
from scraper.miners.races import scrape_races
from scraper.miners.auctions import scrape_auctions
from scraper.miners.hotels import scrape_hotels
from scraper.miners.experiences import scrape_experiences
from scraper.miners.tickets import scrape_tickets
from scraper.miners.trips import scrape_trips

log = logging.getLogger("equitravel.scraper")

MINERS = [
    ("races", scrape_races),
    ("auctions", scrape_auctions),
    ("hotels", scrape_hotels),
    ("experiences", scrape_experiences),
    ("tickets", scrape_tickets),
    ("trips", scrape_trips),
]


async def scrape_all() -> list[dict]:
    """Run all miners and log results."""
    results = []
    for source, miner_fn in MINERS:
        log.info("Running miner: %s", source)
        t0 = time.time()
        try:
            stats = await miner_fn()
            duration = time.time() - t0
            log_entry = ScrapeLog(
                source=source,
                status="success",
                records_found=stats.get("found", 0),
                records_added=stats.get("added", 0),
                records_updated=stats.get("updated", 0),
                duration_seconds=round(duration, 2),
            )
            log.info(
                "  %s: found=%d added=%d updated=%d (%.1fs)",
                source, stats.get("found", 0), stats.get("added", 0),
                stats.get("updated", 0), duration,
            )
        except Exception as exc:
            duration = time.time() - t0
            log_entry = ScrapeLog(
                source=source,
                status="error",
                error_message=str(exc)[:500],
                duration_seconds=round(duration, 2),
            )
            log.error("  %s: FAILED — %s (%.1fs)", source, exc, duration)

        async with async_session() as session:
            session.add(log_entry)
            await session.commit()
        results.append({"source": source, "status": log_entry.status})

    return results
