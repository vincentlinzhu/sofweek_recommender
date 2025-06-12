# Usul: SOFWEEK Conference Recommender

This project demonstrates a minimal end‑to‑end stack for recommending SOFWEEK conference events and speakers. A FastAPI backend stores agenda items in PostgreSQL with the `pgvector` extension. Events and speaker biographies are embedded with a sentence‑transformers model and stored as vectors. A simple React + Vite frontend lets users type in a description of their company and receive recommended agenda items.

**Tech Stack**

- **FastAPI** with SQLAlchemy
- **PostgreSQL** + **pgvector** for vector search
- **sentence-transformers** (`all-MiniLM-L6-v2`) for embeddings
- **BeautifulSoup** scraper (placeholder selectors)
- **React** + **Vite** frontend

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Scraper   │───▶│   PostgreSQL    │◀───│  FastAPI API    │
│  (BeautifulSoup)│    │   + pgvector    │    │   + SQLAlchemy  │
└─────────────────┘    └─────────────────┘    └─────────┬───────┘
                                                        │
                       ┌─────────────────┐              │
                       │  Embedding ETL  │◀──────────────┘
                       │ (transformers)  │              |
                       └─────────────────┘              |
                                                        |   
                                                        │
                                                        ▼
                       ┌─────────────────────────────────────┐
                       │        React + Vite Frontend        │
                       │     (Company → Recommendations)     │
                       └─────────────────────────────────────┘
```

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Docker Setup on macOS](#docker-setup-on-macos)
3. [Clone & Environment Setup](#clone--environment-setup)
4. [Database Setup](#database-setup)
5. [Backend Setup (Python + FastAPI)](#backend-setup-python--fastapi)
6. [Frontend Setup (React + Vite)](#frontend-setup-react--vite)
7. [Running with Docker Compose](#running-with-docker-compose)
8. [Scraping & ETL](#scraping--etl)
9. [API Usage](#api-usage)
10. [Design Notes](#design-notes)
11. [Hourly Scraping](#hourly-scraping)

---

## Prerequisites
- Docker with Docker Compose
- Python 3.11
- Node 18+
- Git

On macOS with Homebrew you can install the tools with:
```bash
brew install git
brew install node       # includes npm
brew install python@3.11
```
Make sure the Docker daemon is running before using `docker-compose`.

---

## Docker Setup on macOS
Docker Desktop

1. Download Docker Desktop from docker.com
2. Install the .dmg file by dragging Docker to Applications
3. Launch Docker Desktop from Applications
4. Wait for Docker to start (you'll see the whale icon in your menu bar)
5. Verify installation:
```bash
docker-compose --version
```

---

## Clone & Environment Setup
```bash
git clone https://github.com/vincentlinzhu/sofweek_recommender.git
cd sofweek_recommender
cp backend/.env.example backend/.env
```

Edit `backend/.env` to set `AGENDA_URL` to the real agenda page. The file also
defines the database URL and embedding model. When running the backend directly
without Docker, replace the `db` hostname with `localhost` in `DATABASE_URL`.

```bash
# inside backend/.env when running locally
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/confrec
```

---

## Database Setup

Make sure PostgreSQL is running and create the `confrec` database:

```bash
createdb confrec
psql -d confrec -f db/init.sql
```

If using Docker, simply start the database service which automatically runs the
`init.sql` script:

```bash
docker-compose up db
```

---

## Backend Setup (Python + FastAPI)

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
uvicorn app.main:app --reload
```
The API will be available on `http://localhost:8000`.

---

## Frontend Setup (React + Vite)
```bash
cd frontend/confrec
npm install
npm run dev
```
The dev server proxies `/recommend`, `/events` and `/speakers` to the backend.

---

## Running with Docker Compose
```bash
docker-compose up --build
```
This launches PostgreSQL with `pgvector`, the FastAPI backend and the scraper service.

## Scraping & ETL
The scraper uses `requests` and `BeautifulSoup` to collect agenda items. Run it manually with:
```bash
python -m backend.app.scrape_runner
```
(or rely on the Docker `scraper` service). After scraping, generate embeddings:
```bash
python -m backend.app.etl
```

---

## API Usage
`POST /recommend`
```json
{
  "company_description": "Counter UAS technology for the Army",
  "k": 5
}
```

Returns the most relevant events or speakers ordered by similarity score.

---

## Design Notes

- Embeddings use 384 dimensions to match the MiniLM model.
- The `pgvector` extension with the `ivfflat` index provides efficient ANN search.
- The project is containerised for easy local development.

---

## Hourly Scraping

The `docker-compose.yml` file includes a `scraper` service that loops every hour:

```yaml
scraper:
  build: ./backend
  command: bash -c "while true; do python -m app.scraper_runner; sleep 3600; done"
```

This service calls `backend/app/scraper_runner.py` which fetches the agenda and stores new events before updating embeddings.
