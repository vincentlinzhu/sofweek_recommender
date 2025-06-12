from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2, sentence_transformers, numpy as np

app   = FastAPI()
model = sentence_transformers.SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
conn  = psycopg2.connect(dsn="dbname=confrec user=...")

class Query(BaseModel):
    company_description: str
    k: int = 10

@app.post("/recommend")
def recommend(q: Query):
    vec = model.encode(q.company_description).astype(np.float32).tolist()
    with conn.cursor() as cur:
        cur.execute("""
            SELECT e.id, e.type, cos_distance(vector, %s) AS score
              FROM embeddings e
          ORDER BY vector <-> %s
             LIMIT %s
        """, (vec, vec, q.k))
        rows = cur.fetchall()
    return rows            # transform to richer JSON on the way out
