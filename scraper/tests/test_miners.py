"""Tests for scraper miners."""

from __future__ import annotations

import asyncio

import pytest
import pytest_asyncio
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from api.database import Base
from api.models import Event, Venue, Region, VendorListing

TEST_DB_URL = "sqlite+aiosqlite:///:memory:"
test_engine = create_async_engine(TEST_DB_URL, echo=False)
TestSession = async_sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def setup_db(monkeypatch):
    """Create tables and patch the session factory used by miners."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Patch the async_session used by miners
    monkeypatch.setattr("api.database.async_session", TestSession)
    yield

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.mark.asyncio
async def test_race_miner(setup_db):
    from scraper.miners.races import scrape_races
    stats = await scrape_races()
    assert stats["found"] > 0
    assert stats["added"] > 0

    async with TestSession() as session:
        count = (await session.execute(select(func.count(Event.id)))).scalar()
        assert count > 10  # Should have many major races


@pytest.mark.asyncio
async def test_auction_miner(setup_db):
    from scraper.miners.auctions import scrape_auctions
    stats = await scrape_auctions()
    assert stats["found"] > 0
    assert stats["added"] > 0

    async with TestSession() as session:
        auctions = (await session.execute(
            select(Event).where(Event.event_type == "auction")
        )).scalars().all()
        assert len(auctions) > 5


@pytest.mark.asyncio
async def test_hotel_miner(setup_db):
    from scraper.miners.hotels import scrape_hotels
    stats = await scrape_hotels()
    assert stats["found"] > 0
    assert stats["added"] > 0

    async with TestSession() as session:
        hotels = (await session.execute(
            select(VendorListing).where(VendorListing.vendor_type == "hotel")
        )).scalars().all()
        assert len(hotels) >= 5


@pytest.mark.asyncio
async def test_experience_miner(setup_db):
    from scraper.miners.experiences import scrape_experiences
    stats = await scrape_experiences()
    assert stats["found"] > 0
    assert stats["added"] > 0


@pytest.mark.asyncio
async def test_idempotent_scrape(setup_db):
    """Running miners twice should not duplicate records."""
    from scraper.miners.races import scrape_races
    stats1 = await scrape_races()
    stats2 = await scrape_races()
    assert stats2["added"] == 0  # All should be updates on second run
    assert stats2["updated"] == stats1["found"]
