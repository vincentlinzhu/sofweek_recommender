from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import SessionLocal
from .. import models, schemas

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get('/events', response_model=list[schemas.EventBase])
def list_events(db: Session = Depends(get_db)):
    return db.query(models.Event).all()