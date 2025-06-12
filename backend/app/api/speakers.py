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

@router.get('/speakers', response_model=list[schemas.SpeakerBase])
def list_speakers(db: Session = Depends(get_db)):
    return db.query(models.Speaker).all()
