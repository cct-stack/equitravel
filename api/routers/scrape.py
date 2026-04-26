"""Scraper status and manual trigger endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.database import get_db
from api.models import ScrapeLog
from api.schemas import ScrapeStatusOut, ScrapeStatusListResponse

router = APIRouter(prefix="/api/scrape", tags=["scrape"])


@router.get("/status", response_model=ScrapeStatusListResponse)
async def scrape_status(db: AsyncSession = Depends(get_db)):
    """Return the last scrape result per source."""
    q = select(ScrapeLog).order_by(ScrapeLog.scraped_at.desc()).limit(50)
    result = await db.execute(q)
    logs = result.scalars().all()
    return ScrapeStatusListResponse(
        logs=[ScrapeStatusOut.model_validate(l) for l in logs],
        total=len(logs),
    )


@router.post("/trigger")
async def trigger_scrape():
    """Manually trigger a full scrape cycle."""
    from api.app import run_scrape_cycle
    import asyncio
    asyncio.create_task(run_scrape_cycle())
    return {"status": "scrape_triggered"}
