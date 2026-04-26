"""APScheduler setup for periodic scraping jobs."""

from __future__ import annotations

import asyncio
import logging
from typing import Callable, Coroutine

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

from api.config import SCRAPE_INTERVAL_HOURS, SCRAPE_DAILY_HOUR

log = logging.getLogger("equitravel.scheduler")


def _run_async(coro_fn: Callable[[], Coroutine]):
    """Wrapper to run async scrape function from sync APScheduler."""
    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(coro_fn())
    finally:
        loop.close()


def start_scheduler(scrape_fn: Callable[[], Coroutine]) -> BackgroundScheduler:
    """Start the background scraping scheduler."""
    scheduler = BackgroundScheduler()

    # Periodic scrape every N hours
    scheduler.add_job(
        _run_async,
        IntervalTrigger(hours=SCRAPE_INTERVAL_HOURS),
        args=[scrape_fn],
        id="periodic_scrape",
        name=f"Scrape every {SCRAPE_INTERVAL_HOURS}h",
        replace_existing=True,
    )

    # Daily deep scrape at configured hour UTC
    scheduler.add_job(
        _run_async,
        CronTrigger(hour=SCRAPE_DAILY_HOUR, minute=0),
        args=[scrape_fn],
        id="daily_scrape",
        name=f"Daily deep scrape at {SCRAPE_DAILY_HOUR}:00 UTC",
        replace_existing=True,
    )

    scheduler.start()
    log.info(
        "Scheduler started: periodic=%dh, daily=%d:00 UTC",
        SCRAPE_INTERVAL_HOURS,
        SCRAPE_DAILY_HOUR,
    )
    return scheduler
