# ── Stage 1: Build React frontend ──────────────────────────────
FROM node:22-alpine AS frontend

WORKDIR /build
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# ── Stage 2: Python API + static assets ────────────────────────
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY api/ ./api/
COPY scraper/ ./scraper/

# Copy built React assets
COPY --from=frontend /build/dist /app/static

ENV EQUITRAVEL_DATA_DIR=/data
ENV STATIC_DIR=/app/static

EXPOSE 8070

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8070"]
