# 🏇 EquiTravel

Horse racing travel platform — a centralized hub for race events, auctions, hotels, restaurants, and luxury experiences worldwide. Built for high-end racing fans, breeders, and auction attendees.

## What's Inside

| Layer | Stack |
|-------|-------|
| **Backend** | FastAPI · async SQLAlchemy · SQLite (swap to Postgres for prod) |
| **Frontend** | React 18 · Vite · Tailwind CSS · Leaflet maps |
| **Scraping** | APScheduler · pluggable miner framework (races, auctions, hotels, experiences, tickets, trips) |
| **Deploy** | Docker-ready · designed for AWS ECS/Fargate |

### Current Data (seeded on first boot)

- **18 major races** — Kentucky Derby, Breeders' Cup, Royal Ascot, Dubai World Cup, Melbourne Cup, Japan Cup, and more
- **14 auctions** — Keeneland, Fasig-Tipton, Tattersalls, Goffs, Magic Millions, Arqana
- **60+ hotels, casinos & restaurants** — with GPS coordinates for map display
- **11 experiences** — bourbon distillery tours, golf, fly fishing, private aviation
- **33 ticket price tiers** and **18 trip cost estimates**

---

## Quick Start

### Prerequisites

- Python 3.10+ (3.10–3.12 recommended)
- Node.js 18+

### 1. Backend

```bash
cd equitravel

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the API (auto-seeds DB on first run)
PYTHONPATH=. uvicorn api.main:app --host 0.0.0.0 --port 8070 --reload
```

The backend will:
- Create `data/equitravel.db` automatically
- Seed all event/vendor/pricing data on first boot
- Start the scraper scheduler (every 6h + daily deep scrape at 4AM UTC)

API docs available at **http://localhost:8070/docs**

### 2. Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npx vite --port 5174
```

Open **http://localhost:5174** in your browser.

### 3. Run Tests

```bash
# From the equitravel root
source .venv/bin/activate
PYTHONPATH=. python -m pytest api/tests/ scraper/tests/ -v
```

---

## Project Structure

```
equitravel/
├── api/                    # FastAPI backend
│   ├── app.py              # App factory
│   ├── config.py           # Environment config
│   ├── database.py         # Async SQLAlchemy setup
│   ├── main.py             # Uvicorn entrypoint
│   ├── models.py           # ORM models (Event, Venue, Region, VendorListing, etc.)
│   ├── schemas.py          # Pydantic response schemas
│   ├── routers/            # API route handlers
│   │   ├── events.py       # /api/events + /api/events/{id} (detail with services)
│   │   ├── vendors.py      # /api/vendors
│   │   ├── venues.py       # /api/venues
│   │   └── scrape.py       # /api/scrape (manual trigger)
│   └── tests/              # Backend tests
├── scraper/                # Data mining engine
│   ├── engine.py           # Runs all miners in sequence
│   ├── scheduler.py        # APScheduler config
│   ├── seed.py             # First-boot seeder
│   ├── data.py             # Curated global racing data (GPS coords, venues)
│   └── miners/             # Pluggable scrapers
│       ├── races.py        # Race events + venues
│       ├── auctions.py     # Auction events
│       ├── hotels.py       # Hotels, casinos, restaurants
│       ├── experiences.py  # Tours, golf, fishing, aviation
│       ├── tickets.py      # Ticket price tiers
│       └── trips.py        # Trip cost estimates
├── frontend/               # React SPA
│   └── src/
│       ├── pages/          # EventsPage, EventDetailPage, VenuesPage, VendorsPage
│       ├── components/     # EventMap (Leaflet), TripEstimate, Header
│       └── hooks/api.ts    # API client + TypeScript interfaces
├── Dockerfile              # Production container
├── requirements.txt        # Python dependencies
└── README.md
```

## Key API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /api/events` | List all events (filterable by type, country) |
| `GET /api/events/{id}` | Full event detail: tickets, hotels, restaurants, map coords, trip estimate |
| `GET /api/vendors` | All vendors (filterable by type) |
| `GET /api/venues` | All venues/tracks |
| `POST /api/scrape` | Manually trigger a scrape cycle |
| `GET /health` | Health check |

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `sqlite+aiosqlite:///data/equitravel.db` | Database connection string |
| `SCRAPE_INTERVAL_HOURS` | `6` | Hours between scrape cycles |
| `SCRAPE_DAILY_HOUR` | `4` | UTC hour for daily deep scrape |
| `SCRAPE_ON_STARTUP` | `0` | Set to `1` to force scrape at boot |

## Roadmap

- [ ] Live scraping from real ticket/hotel APIs (StubHub, Booking.com, etc.)
- [ ] AI trip planner with industry persona chatbots
- [ ] User accounts and saved itineraries
- [ ] Push notifications for price drops and event reminders
- [ ] PostgreSQL + Redis for production deployment
- [ ] Mobile-responsive design

## License

MIT
