"""Pydantic schemas for API request/response serialization."""

from __future__ import annotations

import datetime as dt
from typing import Optional

from pydantic import BaseModel


# ── Region ────────────────────────────────────────────────────────

class RegionOut(BaseModel):
    id: int
    name: str
    country: str
    timezone: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    model_config = {"from_attributes": True}


# ── Venue ─────────────────────────────────────────────────────────

class VenueOut(BaseModel):
    id: int
    name: str
    venue_type: str
    description: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    website: Optional[str] = None
    phone: Optional[str] = None
    price_tier: Optional[str] = None
    image_url: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    rating: Optional[float] = None
    region: Optional[RegionOut] = None
    model_config = {"from_attributes": True}


# ── Event ─────────────────────────────────────────────────────────

class EventOut(BaseModel):
    id: int
    name: str
    event_type: str
    description: Optional[str] = None
    start_date: dt.date
    end_date: Optional[dt.date] = None
    start_time: Optional[str] = None
    purse: Optional[str] = None
    grade: Optional[str] = None
    surface: Optional[str] = None
    distance: Optional[str] = None
    ticket_url: Optional[str] = None
    image_url: Optional[str] = None
    source_url: Optional[str] = None
    venue: Optional[VenueOut] = None
    region: Optional[RegionOut] = None
    model_config = {"from_attributes": True}


class EventListResponse(BaseModel):
    events: list[EventOut]
    total: int
    page: int
    page_size: int


# ── Vendor ────────────────────────────────────────────────────────

class VendorOut(BaseModel):
    id: int
    vendor_name: str
    vendor_type: str
    description: Optional[str] = None
    website: Optional[str] = None
    contact_info: Optional[str] = None
    price_range: Optional[str] = None
    featured: bool = False
    image_url: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    venue: Optional[VenueOut] = None
    model_config = {"from_attributes": True}


# ── Scrape status ─────────────────────────────────────────────────

class ScrapeStatusOut(BaseModel):
    source: str
    status: str
    records_found: int
    records_added: int
    records_updated: int
    error_message: Optional[str] = None
    duration_seconds: Optional[float] = None
    scraped_at: dt.datetime
    model_config = {"from_attributes": True}


class ScrapeStatusListResponse(BaseModel):
    logs: list[ScrapeStatusOut]
    total: int


# ── Pricing ───────────────────────────────────────────────────────

class TicketPriceOut(BaseModel):
    id: int
    source: str
    tier: str
    price_low: float
    price_high: Optional[float] = None
    currency: str = "USD"
    url: Optional[str] = None
    in_stock: bool = True
    scraped_at: dt.datetime
    model_config = {"from_attributes": True}


class HotelRateOut(BaseModel):
    id: int
    vendor_name: str
    vendor_type: str
    check_in: dt.date
    check_out: dt.date
    room_type: str
    rate_per_night: float
    currency: str = "USD"
    source: str
    url: Optional[str] = None
    available: bool = True
    scraped_at: dt.datetime
    model_config = {"from_attributes": True}


# ── Trip estimate ─────────────────────────────────────────────────

class TripEstimateOut(BaseModel):
    nights: int
    currency: str = "USD"
    hotel_low: float
    hotel_high: float
    tickets_low: float
    tickets_high: float
    dining_per_day: float
    experiences_per_day: float
    transport: float
    total_low: float
    total_high: float
    model_config = {"from_attributes": True}


# ── Event detail (full view with services) ────────────────────────

class EventDetailResponse(BaseModel):
    """Full event with all associated services, pricing, and nearby vendors."""
    event: EventOut
    ticket_prices: list[TicketPriceOut] = []
    nearby_hotels: list[VendorOut] = []
    nearby_casinos: list[VendorOut] = []
    nearby_restaurants: list[VendorOut] = []
    nearby_experiences: list[VendorOut] = []
    hotel_rates: list[HotelRateOut] = []
    trip_estimate: Optional[TripEstimateOut] = None
