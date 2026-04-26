"""Shared fixtures for API tests."""

from __future__ import annotations

import asyncio
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from api.database import Base, get_db
from api.app import create_app
from api.models import Region, Venue, Event, VendorListing


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


# In-memory SQLite for tests
TEST_DB_URL = "sqlite+aiosqlite:///:memory:"
test_engine = create_async_engine(TEST_DB_URL, echo=False)
TestSession = async_sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)


@pytest_asyncio.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with TestSession() as session:
        yield session
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def seeded_db(db_session: AsyncSession) -> AsyncSession:
    """DB with some test data."""
    region = Region(name="Kentucky", country="USA", timezone="US/Eastern")
    db_session.add(region)
    await db_session.flush()

    venue = Venue(name="Churchill Downs", venue_type="track", region_id=region.id)
    db_session.add(venue)
    await db_session.flush()

    from datetime import date
    event = Event(
        name="Kentucky Derby 152",
        event_type="race",
        start_date=date(2026, 5, 2),
        grade="G1",
        purse="$5,000,000",
        surface="Dirt",
        distance="1¼ miles",
        venue_id=venue.id,
        region_id=region.id,
    )
    db_session.add(event)

    vendor = VendorListing(
        vendor_name="The Brown Hotel",
        vendor_type="hotel",
        description="Historic luxury hotel",
        price_range="$350-800/night",
        region_id=region.id,
    )
    db_session.add(vendor)
    await db_session.commit()
    return db_session


@pytest_asyncio.fixture
async def client(seeded_db: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Test client with seeded DB."""
    app = create_app()

    async def override_get_db():
        yield seeded_db

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c
