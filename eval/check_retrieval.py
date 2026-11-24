import json
import sqlglot
from sqlglot import exp
from rag.retriever import retrieve

hits = total = 0
for line in open("eval/questions.jsonl"):
    if not line.strip():
        continue
    q = json.loads(line)
    total += 1
    needed = {t.name for t in sqlglot.parse_one(q["sql"], read="postgres").find_all(exp.Table)}
    found = retrieve(q["question"])[0]
    missing = needed - found
    if missing:
        print(q["id"], "MISSING", sorted(missing))
    else:
        hits += 1
print(f"Retrieval: {hits}/{total} questions had every needed table = {hits / total:.0%}")