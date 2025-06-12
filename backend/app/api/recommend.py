from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from ..db import SessionLocal
from .. import models, schemas
from sentence_transformers import SentenceTransformer
from sqlalchemy import text
import numpy as np
import os

router = APIRouter()
model_name = os.getenv('SENTENCE_MODEL', 'sentence-transformers/all-MiniLM-L6-v2')
model = SentenceTransformer(model_name)

class RecQuery(BaseModel):
    company_description: str
    k: int = 5


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post('/recommend', response_model=list[schemas.Recommendation])
def recommend(q: RecQuery, db: Session = Depends(get_db)):
    vec = model.encode(q.company_description).astype(np.float32).tolist()
    sql = text(
        "SELECT id, type, 1 - (vector <=> :vec) AS score "
        "FROM embeddings ORDER BY vector <-> :vec LIMIT :k"
    )
    rows = db.execute(sql, {"vec": vec, "k": q.k}).fetchall()
    return [schemas.Recommendation(id=r[0], type=r[1], score=r[2]) for r in rows]