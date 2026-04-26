"""Tests for the events API."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_list_events(client: AsyncClient):
    resp = await client.get("/api/events", params={"from_date": "2026-01-01"})
    assert resp.status_code == 200
    data = resp.json()
    assert "events" in data
    assert "total" in data
    assert data["total"] >= 1
    # Should have Kentucky Derby
    names = [e["name"] for e in data["events"]]
    assert "Kentucky Derby 152" in names


@pytest.mark.asyncio
async def test_filter_by_type(client: AsyncClient):
    resp = await client.get("/api/events", params={"event_type": "race", "from_date": "2026-01-01"})
    assert resp.status_code == 200
    data = resp.json()
    for e in data["events"]:
        assert e["event_type"] == "race"


@pytest.mark.asyncio
async def test_filter_by_country(client: AsyncClient):
    resp = await client.get("/api/events", params={"country": "USA", "from_date": "2026-01-01"})
    assert resp.status_code == 200
    data = resp.json()
    for e in data["events"]:
        assert e["region"]["country"] == "USA"


@pytest.mark.asyncio
async def test_event_detail(client: AsyncClient):
    # Get list first to find an ID
    resp = await client.get("/api/events", params={"from_date": "2026-01-01"})
    events = resp.json()["events"]
    assert len(events) > 0

    event_id = events[0]["id"]
    resp = await client.get(f"/api/events/{event_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["event"]["id"] == event_id
    assert "name" in data["event"]
    assert "ticket_prices" in data
    assert "nearby_hotels" in data
    assert "nearby_restaurants" in data
    assert "nearby_experiences" in data


@pytest.mark.asyncio
async def test_event_not_found(client: AsyncClient):
    resp = await client.get("/api/events/99999")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_event_has_venue(client: AsyncClient):
    resp = await client.get("/api/events", params={"from_date": "2026-01-01"})
    events = resp.json()["events"]
    derby = next(e for e in events if e["name"] == "Kentucky Derby 152")
    assert derby["venue"] is not None
    assert derby["venue"]["name"] == "Churchill Downs"


@pytest.mark.asyncio
async def test_event_has_region(client: AsyncClient):
    resp = await client.get("/api/events", params={"from_date": "2026-01-01"})
    events = resp.json()["events"]
    derby = next(e for e in events if e["name"] == "Kentucky Derby 152")
    assert derby["region"]["country"] == "USA"
    assert derby["region"]["name"] == "Kentucky"
