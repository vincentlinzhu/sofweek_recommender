DROP DATABASE IF EXISTS confrec;
CREATE DATABASE confrec;
\c confrec;

CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS events (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    starts_at TIMESTAMP,
    location TEXT
);

CREATE TABLE IF NOT EXISTS speakers (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    biography TEXT
);

CREATE TABLE IF NOT EXISTS event_speakers (
    event_id INTEGER REFERENCES events(id) ON DELETE CASCADE,
    speaker_id INTEGER REFERENCES speakers(id) ON DELETE CASCADE,
    PRIMARY KEY (event_id, speaker_id)
);

-- Embeddings for both events and speakers
CREATE TABLE IF NOT EXISTS embeddings (
    id INTEGER NOT NULL,
    type TEXT NOT NULL, -- 'event' or 'speaker'
    vector vector(384),
    PRIMARY KEY (id, type)
);
CREATE INDEX IF NOT EXISTS embeddings_vector_idx ON embeddings USING ivfflat (vector vector_cosine_ops);
