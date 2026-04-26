"""Tests for the vendors API."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_list_vendors(client: AsyncClient):
    resp = await client.get("/api/vendors")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) >= 1


@pytest.mark.asyncio
async def test_filter_by_type(client: AsyncClient):
    resp = await client.get("/api/vendors", params={"vendor_type": "hotel"})
    assert resp.status_code == 200
    data = resp.json()
    for v in data:
        assert v["vendor_type"] == "hotel"


@pytest.mark.asyncio
async def test_vendor_has_fields(client: AsyncClient):
    resp = await client.get("/api/vendors")
    vendor = resp.json()[0]
    assert "vendor_name" in vendor
    assert "vendor_type" in vendor
    assert "description" in vendor
