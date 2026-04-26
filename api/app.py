"""EquiTravel — FastAPI application factory."""

from __future__ import annotations

import asyncio
import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from api.config import STATIC_DIR
from api.database import init_db

log = logging.getLogger("equitravel")


async def run_scrape_cycle():
    """Run a full scrape cycle (called by scheduler or manual trigger)."""
    from scraper.engine import scrape_all
    try:
        await scrape_all()
    except Exception as exc:
        log.error("Scrape cycle failed: %s", exc, exc_info=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup/shutdown lifecycle."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
        datefmt="%H:%M:%S",
    )
    log.info("Initializing database…")
    await init_db()

    # Seed data on first run
    from scraper.seed import seed_if_empty
    await seed_if_empty()

    # Start scheduler
    from scraper.scheduler import start_scheduler
    scheduler = start_scheduler(run_scrape_cycle)
    log.info("Scraper scheduler started")

    yield

    scheduler.shutdown(wait=False)
    log.info("Shutdown complete")


def create_app() -> FastAPI:
    app = FastAPI(
        title="EquiTravel",
        description="Horse Racing Travel Platform — events, venues, and travel intelligence",
        version="0.1.0",
        lifespan=lifespan,
    )

    # Register routers
    from api.routers.events import router as events_router
    from api.routers.venues import router as venues_router
    from api.routers.vendors import router as vendors_router
    from api.routers.scrape import router as scrape_router

    app.include_router(events_router)
    app.include_router(venues_router)
    app.include_router(vendors_router)
    app.include_router(scrape_router)

    # Health check
    @app.get("/api/health")
    async def health():
        return {"status": "ok", "service": "equitravel"}

    # Serve React SPA (must be last)
    static_path = Path(STATIC_DIR)
    if static_path.exists():
        app.mount("/", StaticFiles(directory=str(static_path), html=True), name="static")

    return app


app = create_app()
