import json
import sys
import time
from step1_chain import sql_chain, SCHEMA
from safety import validate
from db import run_query, log_question
from rag.retriever import retrieve
from pipeline import get_data

STAGE = "eval_retry"
MAX_QUESTIONS = int(sys.argv[1]) if len(sys.argv) > 1 else None

def same_result(a, b):       #Compares the AI's result with correct result. 
    if a.shape != b.shape:
        return False
    rows_a = sorted(a.round(2).astype(str).values.tolist())
    rows_b = sorted(b.round(2).astype(str).values.tolist())
    return rows_a == rows_b

correct = total = 0
for line in open("eval/questions.jsonl"):
    if not line.strip():
        continue
    if MAX_QUESTIONS and total >= MAX_QUESTIONS:
        break
    q = json.loads(line)
    total += 1
    start = time.perf_counter()
    sql, rows = None, None
    try:
        gold = run_query(q["sql"])
        sql, result = get_data(q["question"])
        rows = len(result)
        ok = same_result(gold, result)
        status = "eval_ok" if ok else "eval_wrong"
    except Exception as error:
        ok = False
        status = "eval_error"
        print("ERROR", q["id"], error)
    seconds = time.perf_counter() - start
    log_question(f"[test {q['id']}] {q['question']}", STAGE, sql, rows, status, seconds)
    correct += ok
    print(q["id"], "OK" if ok else "WRONG", f"({seconds:.1f}s)")
print(f"Accuracy: {correct}/{total} = {correct / total:.0%}")

#python -m eval.run_eval 5