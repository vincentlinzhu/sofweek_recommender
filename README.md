# Usul: Sofweek Recommender

Problem Statement:
Defense companies go to conferences like SOFWEEK to attend events and find people they should talk to. Make a supercharged app to recommend events and people to talk to for companies. Scrape the Agenda website for the biographies of the speakers and the events. Given a description of a company, i.e., Counter UAS Companies working for the Army. Recommend events and people that we should talk to. Make a simple frontend to host it all.

My Specifications:
I want a React + Vite frontend. I want a FastAPI Python backend with a PostgeSQL db for storing and displaying the events and people, as well as a vector database for recommendations. The scraper could use something such as beautifulsoup and requests, and have it hosted and run every hour (please suggest a method). Can you also suggest a recommendation engine from Huggingface, as well as a vectorizer such as word2vec? The recommendation engine should work with a natural language description of the user's preferences and then return the suggestions in a nice frontend.

# Usul: SOFWEEK Conference Recommender

A **supercharged** event-and-speaker recommendation system for defense companies attending SOFWEEK (and similar conferences).  

Built with:
- **FastAPI** + **PostgreSQL** (+ pgvector) backend  
- **React** + **Vite** frontend  
- **BeautifulSoup** & **requests** scraper  
- **Sentence-Transformers** embedding + pgvector ANN search  

                         ┌─────────────────────┐
   Agenda URL(s) ──▶     │  Scraper service    │───►  Raw JSON
                         │ (requests + BS4)    │
                         └────────┬────────────┘
                                  │
                                  ▼
                         ┌─────────────────────┐
                         │  ETL / Embedding    │───►  pgvector
                         │  (Sentence-TF)      │
 Company free-text ──▶   └────────┬────────────┘
                                  │
                                  ▼
                         ┌─────────────────────┐
                         │ FastAPI backend     │
                         │  • /recommend       │
                         │  • /events          │
                         │  • /speakers        │
                         └────────┬────────────┘
                                  │ JSON/HTTPS
                                  ▼
                         ┌─────────────────────┐
                         │ React + Vite UI     │
                         └─────────────────────┘

---

## Table of Contents

1. [Prerequisites](#prerequisites)  
2. [Clone & Environment Setup](#clone--environment-setup)  
3. [Database Initialization](#database-initialization)  
4. [Scraper: Pull Agenda Data](#scraper-pull-agenda-data)  
5. [ETL & Embeddings](#etl--embeddings)  
6. [Backend Setup (FastAPI)](#backend-setup-fastapi)  
7. [Frontend Setup (React + Vite)](#frontend-setup-react--vite)  
8. [Docker Compose (Dev)](#docker-compose-dev)  
9. [Design Decisions](#design-decisions)  
10. [Next Steps](#next-steps)

---

## Prerequisites

On macOS / Linux:

1. **Docker & Docker Compose**  
2. **Python 3.11+** & **pip**  
3. **Node 18+** & **npm**  
4. (Optional) `psql` client if you prefer manual DB work

---

## Clone & Environment Setup

```bash
git clone https://github.com/vincentlinzhu/sofweek_recommender.git
cd sofweek_recommender

