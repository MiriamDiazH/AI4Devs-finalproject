CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS patients (
    id          VARCHAR PRIMARY KEY,
    name        VARCHAR(255) NOT NULL,
    birth_date  DATE NOT NULL,
    sex         VARCHAR(10) NOT NULL
);

CREATE TABLE IF NOT EXISTS encounters (
    id          VARCHAR PRIMARY KEY,
    patient_id  VARCHAR NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    date        DATE NOT NULL,
    type        VARCHAR(100) NOT NULL,
    note_text   TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS clinical_events (
    id            VARCHAR PRIMARY KEY,
    encounter_id  VARCHAR NOT NULL REFERENCES encounters(id) ON DELETE CASCADE,
    patient_id    VARCHAR NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    category      VARCHAR(50) NOT NULL,
    title         VARCHAR(255) NOT NULL,
    description   TEXT NOT NULL,
    source_quote  TEXT NOT NULL,
    confidence    FLOAT NOT NULL DEFAULT 0.0,
    event_date    DATE
);

CREATE TABLE IF NOT EXISTS audit_logs (
    id           VARCHAR PRIMARY KEY,
    entity_type  VARCHAR(50) NOT NULL,
    entity_id    VARCHAR NOT NULL,
    action       VARCHAR(50) NOT NULL,
    detail       TEXT,
    created_at   TIMESTAMP NOT NULL DEFAULT NOW()
);
