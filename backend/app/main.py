from fastapi import FastAPI
from .api import events, speakers, recommend

app = FastAPI()

app.include_router(events.router)
app.include_router(speakers.router)
app.include_router(recommend.router)