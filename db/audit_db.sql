CREATE ROLE audit_writer LOGIN PASSWORD 'audit_pw';
REVOKE CONNECT ON DATABASE audit_db FROM PUBLIC; 
GRANT CONNECT ON DATABASE audit_db TO audit_writer;

CREATE TABLE audit_log (                    --one row per question asked 
  id         SERIAL PRIMARY KEY,
  asked_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
  question   TEXT NOT NULL,
  intent     TEXT,
  sql_text   TEXT,
  row_count  INTEGER,
  status     TEXT NOT NULL,
  seconds    REAL
);
GRANT SELECT, INSERT ON audit_log TO audit_writer;
GRANT USAGE ON SEQUENCE audit_log_id_seq TO audit_writer;