"""Tests for the venues API."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_list_venues(client: AsyncClient):
    resp = await client.get("/api/venues")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert data[0]["name"] == "Churchill Downs"


@pytest.mark.asyncio
async def test_filter_by_type(client: AsyncClient):
    resp = await client.get("/api/venues", params={"venue_type": "track"})
    assert resp.status_code == 200
    data = resp.json()
    for v in data:
        assert v["venue_type"] == "track"


@pytest.mark.asyncio
async def test_venue_detail(client: AsyncClient):
    resp = await client.get("/api/venues")
    venues = resp.json()
    venue_id = venues[0]["id"]

    resp = await client.get(f"/api/venues/{venue_id}")
    assert resp.status_code == 200
    assert resp.json()["id"] == venue_id


@pytest.mark.asyncio
async def test_venue_not_found(client: AsyncClient):
    resp = await client.get("/api/venues/99999")
    assert resp.status_code == 404
