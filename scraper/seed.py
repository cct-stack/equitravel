"""First-run seed — populates the DB if empty."""

from __future__ import annotations

import logging

from sqlalchemy import select, func

from api.database import async_session
from api.models import Event

log = logging.getLogger("equitravel.seed")


async def seed_if_empty() -> None:
    """Run the full scrape cycle once if the DB is empty."""
    async with async_session() as session:
        count = (await session.execute(select(func.count(Event.id)))).scalar() or 0

    if count > 0:
        log.info("DB already has %d events — skipping seed", count)
        return

    log.info("Empty DB — running initial seed…")
    from scraper.engine import scrape_all
    await scrape_all()
    log.info("Seed complete")
