"""SQLAlchemy ORM models for EquiTravel."""

from __future__ import annotations

import datetime as dt
from typing import Optional

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


# ── Region (geographic grouping) ─────────────────────────────────


class Region(Base):
    __tablename__ = "regions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, index=True)  # "Kentucky", "Dubai", "Hong Kong"
    country: Mapped[str] = mapped_column(String(80), index=True)
    timezone: Mapped[str] = mapped_column(String(60), default="UTC")
    latitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    longitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    venues: Mapped[list["Venue"]] = relationship(back_populates="region")
    events: Mapped[list["Event"]] = relationship(back_populates="region")


# ── Venue (tracks, casinos, hotels, restaurants, experiences) ────


class Venue(Base):
    __tablename__ = "venues"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200), index=True)
    venue_type: Mapped[str] = mapped_column(String(40), index=True)  # track | casino | hotel | restaurant | experience | auction_house
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    address: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)
    city: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    website: Mapped[Optional[str]] = mapped_column(String(400), nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    price_tier: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)  # $, $$, $$$, $$$$
    image_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    latitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    longitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    rating: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    region_id: Mapped[Optional[int]] = mapped_column(ForeignKey("regions.id"), nullable=True)
    region: Mapped[Optional["Region"]] = relationship(back_populates="venues")

    events: Mapped[list["Event"]] = relationship(back_populates="venue")
    vendor_listings: Mapped[list["VendorListing"]] = relationship(back_populates="venue")

    created_at: Mapped[dt.datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[dt.datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())


# ── Event (races, auctions, festivals, experiences) ──────────────


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(300), index=True)
    event_type: Mapped[str] = mapped_column(String(40), index=True)  # race | auction | festival | experience
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    start_date: Mapped[dt.date] = mapped_column(index=True)
    end_date: Mapped[Optional[dt.date]] = mapped_column(nullable=True)
    start_time: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)  # "14:30"
    purse: Mapped[Optional[str]] = mapped_column(String(60), nullable=True)  # "$7,000,000"
    grade: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)  # "G1", "G2", "Listed"
    surface: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)  # "Dirt", "Turf", "AW"
    distance: Mapped[Optional[str]] = mapped_column(String(40), nullable=True)  # "1¼ miles"
    ticket_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    image_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    source_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    venue_id: Mapped[Optional[int]] = mapped_column(ForeignKey("venues.id"), nullable=True)
    venue: Mapped[Optional["Venue"]] = relationship(back_populates="events")

    region_id: Mapped[Optional[int]] = mapped_column(ForeignKey("regions.id"), nullable=True)
    region: Mapped[Optional["Region"]] = relationship(back_populates="events")

    ticket_prices: Mapped[list["TicketPrice"]] = relationship(back_populates="event", cascade="all, delete-orphan")

    created_at: Mapped[dt.datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[dt.datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())



# ── Vendor / partner listing ─────────────────────────────────────


class VendorListing(Base):
    __tablename__ = "vendor_listings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    vendor_name: Mapped[str] = mapped_column(String(200), index=True)
    vendor_type: Mapped[str] = mapped_column(String(40), index=True)  # hotel | casino | restaurant | charter | tour | golf | fishing
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    website: Mapped[Optional[str]] = mapped_column(String(400), nullable=True)
    contact_info: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)
    price_range: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    featured: Mapped[bool] = mapped_column(default=False)  # paid/partner listing
    image_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    latitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    longitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    venue_id: Mapped[Optional[int]] = mapped_column(ForeignKey("venues.id"), nullable=True)
    venue: Mapped[Optional["Venue"]] = relationship(back_populates="vendor_listings")

    region_id: Mapped[Optional[int]] = mapped_column(ForeignKey("regions.id"), nullable=True)

    created_at: Mapped[dt.datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[dt.datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())


# ── Scrape log (tracks what was scraped and when) ────────────────


class ScrapeLog(Base):
    __tablename__ = "scrape_log"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    source: Mapped[str] = mapped_column(String(100), index=True)  # "breeders_cup", "keeneland_auctions", etc.
    status: Mapped[str] = mapped_column(String(20))  # "success" | "error" | "partial"
    records_found: Mapped[int] = mapped_column(Integer, default=0)
    records_added: Mapped[int] = mapped_column(Integer, default=0)
    records_updated: Mapped[int] = mapped_column(Integer, default=0)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    duration_seconds: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    scraped_at: Mapped[dt.datetime] = mapped_column(DateTime, server_default=func.now())


# ── Ticket / pricing data ────────────────────────────────────────


class TicketPrice(Base):
    __tablename__ = "ticket_prices"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"), index=True)
    source: Mapped[str] = mapped_column(String(60))  # "ticketmaster", "stubhub", "official"
    tier: Mapped[str] = mapped_column(String(100))  # "General Admission", "Clubhouse", "VIP Box"
    price_low: Mapped[float] = mapped_column(Float)
    price_high: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    currency: Mapped[str] = mapped_column(String(3), default="USD")
    url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    in_stock: Mapped[bool] = mapped_column(Boolean, default=True)
    scraped_at: Mapped[dt.datetime] = mapped_column(DateTime, server_default=func.now())

    event: Mapped["Event"] = relationship(back_populates="ticket_prices")


# ── Hotel rate data ──────────────────────────────────────────────


class HotelRate(Base):
    __tablename__ = "hotel_rates"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    vendor_id: Mapped[int] = mapped_column(ForeignKey("vendor_listings.id"), index=True)
    event_id: Mapped[Optional[int]] = mapped_column(ForeignKey("events.id"), nullable=True, index=True)
    check_in: Mapped[dt.date] = mapped_column()
    check_out: Mapped[dt.date] = mapped_column()
    room_type: Mapped[str] = mapped_column(String(100))  # "Standard King", "Suite"
    rate_per_night: Mapped[float] = mapped_column(Float)
    currency: Mapped[str] = mapped_column(String(3), default="USD")
    source: Mapped[str] = mapped_column(String(60))  # "direct", "booking.com", etc.
    url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    available: Mapped[bool] = mapped_column(Boolean, default=True)
    scraped_at: Mapped[dt.datetime] = mapped_column(DateTime, server_default=func.now())

    vendor: Mapped["VendorListing"] = relationship()
    event: Mapped[Optional["Event"]] = relationship()


# ── Trip cost estimate ────────────────────────────────────────────


class TripEstimate(Base):
    __tablename__ = "trip_estimates"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"), index=True)
    nights: Mapped[int] = mapped_column(Integer)
    currency: Mapped[str] = mapped_column(String(3), default="USD")
    hotel_low: Mapped[float] = mapped_column(Float)  # per night
    hotel_high: Mapped[float] = mapped_column(Float)
    tickets_low: Mapped[float] = mapped_column(Float)
    tickets_high: Mapped[float] = mapped_column(Float)
    dining_per_day: Mapped[float] = mapped_column(Float)
    experiences_per_day: Mapped[float] = mapped_column(Float)
    transport: Mapped[float] = mapped_column(Float)  # flights/car
    total_low: Mapped[float] = mapped_column(Float)
    total_high: Mapped[float] = mapped_column(Float)

    event: Mapped["Event"] = relationship()