"""Simple ETL to embed events and speakers into pgvector."""
import os
from sqlalchemy.orm import Session
from sentence_transformers import SentenceTransformer
import numpy as np
from .db import SessionLocal, engine, Base
from . import models

model_name = os.getenv('SENTENCE_MODEL', 'sentence-transformers/all-MiniLM-L6-v2')
model = SentenceTransformer(model_name)


def run():
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()
    try:
        for event in db.query(models.Event).all():
            vec = model.encode(event.title + " " + (event.description or "")).astype(np.float32)
            emb = models.Embedding(id=event.id, type='event', vector=vec)
            db.merge(emb)
        for spk in db.query(models.Speaker).all():
            vec = model.encode(spk.name + " " + (spk.biography or "")).astype(np.float32)
            emb = models.Embedding(id=spk.id, type='speaker', vector=vec)
            db.merge(emb)
        db.commit()
    finally:
        db.close()

if __name__ == '__main__':
    run()
    