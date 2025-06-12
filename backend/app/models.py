from sqlalchemy import Column, Integer, Text, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from .db import Base

class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(Text, nullable=False)
    description = Column(Text)
    starts_at = Column(DateTime)
    location = Column(Text)
    speakers = relationship('Speaker', secondary='event_speakers', back_populates='events')

class Speaker(Base):
    __tablename__ = 'speakers'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)
    biography = Column(Text)
    events = relationship('Event', secondary='event_speakers', back_populates='speakers')

EventSpeaker = Table(
    'event_speakers', Base.metadata,
    Column('event_id', Integer, ForeignKey('events.id', ondelete='CASCADE'), primary_key=True),
    Column('speaker_id', Integer, ForeignKey('speakers.id', ondelete='CASCADE'), primary_key=True),
)

class Embedding(Base):
    __tablename__ = 'embeddings'
    id = Column(Integer, primary_key=True)
    type = Column(Text, primary_key=True)
    vector = Column(Vector(384))
