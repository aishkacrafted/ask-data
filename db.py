import pandas as pd
from sqlalchemy import create_engine, text

READER_URL = "postgresql+psycopg://ai_reader:reader_pw@localhost:5432/northwind"  #connects as read-only AI login
AUDIT_URL = "postgresql+psycopg://audit_writer:audit_pw@localhost:5432/audit_db"  #for logging questions and answer

reader = create_engine(READER_URL)
audit = create_engine(AUDIT_URL)

def run_query(sql):    #runs a query and returns the result as a table
    with reader.connect() as conn:
        return pd.read_sql(text(sql), conn)

def log_question(question, intent, sql, row_count, status, seconds):
    with audit.begin() as conn:
        conn.execute(
            text("INSERT INTO audit_log (question, intent, sql_text, row_count, status, seconds) "
                 "VALUES (:q, :i, :s, :r, :st, :sec)"),
            {"q": question, "i": intent, "s": sql, "r": row_count, "st": status, "sec": seconds},
        )
