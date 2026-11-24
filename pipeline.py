from agents.agent2 import sql_chain
from rag.retriever import retrieve
from safety import validate
from db import run_query
import time
from agents.agent1 import intent_chain, explain_chain
from db import log_question

def get_data(question):
    names, context = retrieve(question)
    request = question
    for attempt in range(3):  # first try + 2 retries
        sql = sql_chain.invoke({"schema": context, "request": request})
        try:
            sql = validate(sql)
            return sql, run_query(sql)
        except Exception as error:
            request = (f"{question}\nYour previous SQL:\n{sql}\n"
                       f"failed with: {error}\nWrite a corrected query.")
    raise RuntimeError("Could not build a working query")

def ask(question):
    start = time.perf_counter()
    intent = intent_chain.invoke({"message": question}).intent
    if intent == "write":
        log_question(question, intent, None, None, "refused", time.perf_counter() - start)
        return {"text": "I can only read data. I can't add, change or delete anything."}
    try:
        sql, df = get_data(question)
    except RuntimeError:
        log_question(question, intent, None, None, "failed", time.perf_counter() - start)
        return {"text": "Sorry, I couldn't answer that. Try rephrasing it."}
    explanation = explain_chain.invoke({"question": question, "sql": sql})
    log_question(question, intent, sql, len(df), "ok", time.perf_counter() - start)
    return {"text": f"{explanation} Found {len(df)} rows.", "sql": sql, "data": df}