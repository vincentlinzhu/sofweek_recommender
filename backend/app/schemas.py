from datetime import datetime
from pydantic import BaseModel
from typing import List

class SpeakerBase(BaseModel):
    id: int
    name: str
    biography: str | None = None

    class Config:
        from_attributes = True

class EventBase(BaseModel):
    id: int
    title: str
    description: str | None = None
    starts_at: datetime | None = None
    location: str | None = None
    speakers: List[SpeakerBase] = []

    class Config:
        from_attributes = True

class Recommendation(BaseModel):
    id: int
    type: str
    score: float
    