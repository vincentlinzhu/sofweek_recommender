# Usul: SOFWEEK Conference Recommender

This project demonstrates a minimal end‑to‑end stack for recommending SOFWEEK conference events and speakers. A FastAPI backend stores agenda items in PostgreSQL with the `pgvector` extension. Events and speaker biographies are embedded with a sentence‑transformers model and stored as vectors. A simple React + Vite frontend lets users type in a description of their company and receive recommended agenda items.

**Tech Stack**

- **FastAPI** with SQLAlchemy
- **PostgreSQL** + **pgvector** for vector search
- **sentence-transformers** (`all-MiniLM-L6-v2`) for embeddings
- **BeautifulSoup** scraper (placeholder selectors)
- **React** + **Vite** frontend

```
┌─────────────┐        ┌──────────────┐        ┌───────────────────┐
│  scraper    │  --->  │   database   │  --->  │   FastAPI backend │
└─────────────┘        └──────┬───────┘        └─────────┬─────────┘
                               │ JSON/REST                │
                               ▼                          ▼
                         React + Vite frontend      Embedding ETL
```

## Getting Started

### Prerequisites

- Docker & Docker Compose
- Python 3.11+
- Node 18+

### Clone & Setup
```bash
git clone https://github.com/vincentlinzhu/sofweek_recommender.git
cd sofweek_recommender
cp backend/.env.example backend/.env
```

### Run with Docker

```bash
docker-compose up --build
```

The backend will be available on `http://localhost:8000` and the database on port `5432`.

### Frontend

```
cd frontend/confrec
npm install
npm run dev
```

The React app talks to `/recommend`, `/events`, and `/speakers` served by FastAPI.

## Scraper

`backend/app/scraper.py` contains a placeholder scraper using `requests` and `BeautifulSoup`. Adjust the CSS selectors to match the real agenda website. Run it hourly via `cron` or a scheduled container to keep the database fresh.

## ETL

After inserting new events or speakers, run:

```bash
python -m backend.app.etl
```

This computes embeddings and stores them in the `embeddings` table so the `/recommend` endpoint can perform vector search.

## Recommendation API

`POST /recommend`

```json
{
  "company_description": "Counter UAS technology for the Army",
  "k": 5
}
```

Returns a list of items sorted by vector similarity.

## Design Notes

- Embeddings use 384 dimensions to match the MiniLM model.
- The `pgvector` extension with the `ivfflat` index provides efficient ANN search.
- The project is containerised for easy local development.

## Hourly Scraping

One simple approach is to run the scraper inside a small Docker container with the command scheduled by `cron` (`*/60 * * * *`). Another option is to use a CI/CD pipeline or serverless function triggered hourly.

## Next Steps

- Build out real scraper selectors and populate the database.
- Polish the React UI to display recommended events and speaker bios.
- Add authentication if needed.
