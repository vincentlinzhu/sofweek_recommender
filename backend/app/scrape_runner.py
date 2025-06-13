import os
import json
from .scraper import fetch_agenda
from .db import SessionLocal, engine, Base
from .models import Event, Speaker
from .etl import run as run_etl
import datetime


def run() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        url = os.getenv("AGENDA_URL", "https://example.com")
        events = fetch_agenda(url)
        json_path = os.getenv("SCRAPE_JSON_PATH")
        if json_path:
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(events, f, ensure_ascii=False, indent=2)
        for ev in events:
            if not ev.get("title"):
                continue
            existing = db.query(Event).filter_by(title=ev.get("title")).first()
            if not existing:
                existing = Event(title=ev.get("title"))
            existing.description = ev.get("description")
            existing.location = ev.get("location")
            starts_at = ev.get("starts_at")
            if isinstance(starts_at, str):
                try:
                    starts_at = datetime.datetime.fromisoformat(starts_at)
                except Exception:
                    starts_at = None
            existing.starts_at = starts_at
            db.add(existing)
            for name in ev.get("speakers", []):
                sp = db.query(Speaker).filter_by(name=name).first()
                if not sp:
                    sp = Speaker(name=name)
                    db.add(sp)
                    db.flush()
                if sp not in existing.speakers:
                    existing.speakers.append(sp)
        db.commit()
    finally:
        db.close()
    run_etl()


if __name__ == "__main__":
    run()
    