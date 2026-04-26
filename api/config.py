"""Application configuration — reads from env vars with sensible defaults."""

from __future__ import annotations

import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = Path(os.environ.get("EQUITRAVEL_DATA_DIR", str(BASE_DIR / "data")))
DB_PATH = DATA_DIR / "equitravel.db"
DATABASE_URL = os.environ.get(
    "DATABASE_URL", f"sqlite+aiosqlite:///{DB_PATH}"
)

# Scraper schedule — set SCRAPE_INTERVAL_HOURS=1 for hourly
SCRAPE_INTERVAL_HOURS = int(os.environ.get("SCRAPE_INTERVAL_HOURS", "6"))
SCRAPE_DAILY_HOUR = int(os.environ.get("SCRAPE_DAILY_HOUR", "4"))  # 4 AM UTC
# Set SCRAPE_ON_STARTUP=1 to force a full scrape at boot
SCRAPE_ON_STARTUP = os.environ.get("SCRAPE_ON_STARTUP", "0") == "1"

# Server
HOST = os.environ.get("HOST", "0.0.0.0")
PORT = int(os.environ.get("PORT", "8070"))
STATIC_DIR = os.environ.get("STATIC_DIR", str(BASE_DIR / "frontend" / "dist"))

# Ensure data dir exists
DATA_DIR.mkdir(parents=True, exist_ok=True)
