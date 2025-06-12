import os
from .scraper import fetch_agenda
from .db import SessionLocal, engine, Base
from .models import Event
from .etl import run as run_etl


def run() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        url = os.getenv("AGENDA_URL", "https://example.com/agenda")
        events = fetch_agenda(url)
        for ev in events:
            existing = db.query(Event).filter_by(title=ev.get("title")).first()
            if not existing:
                db.add(Event(title=ev.get("title"), description=ev.get("description")))
        db.commit()
    finally:
        db.close()
    run_etl()


if __name__ == "__main__":
    run()
    