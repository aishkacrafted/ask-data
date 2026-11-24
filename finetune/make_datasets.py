import json, random
from datasets import load_dataset
from prompts import SQL_SYS, INTENT_SYS, EXPLAIN_SYS        

WRITE_WORDS = {"INSERT", "UPDATE", "DELETE", "CREATE", "DROP", "ALTER"}


def chat(system, user, answer):
    return {"messages": [{"role": "system", "content": system},
                         {"role": "user", "content": user},
                         {"role": "assistant", "content": answer}]}


def first_word(sql):
    return sql.strip().split()[0].upper() if sql.strip() else ""


rows = load_dataset("gretelai/synthetic_text_to_sql", split="train").shuffle(seed=42).select(range(20000))
reads = [r for r in rows if first_word(r["sql"]) == "SELECT"]
writes = [r for r in rows if first_word(r["sql"]) in WRITE_WORDS]
print(len(reads), "reads,", len(writes), "writes")

agent2 = [chat(SQL_SYS, f"SCHEMA:\n{r['sql_context']}\nREQUEST: {r['sql_prompt']}", r["sql"])
          for r in reads[:2000]]
agent1 = ([chat(INTENT_SYS, r["sql_prompt"], json.dumps({"intent": "read"})) for r in reads[2000:2600]]
        + [chat(INTENT_SYS, r["sql_prompt"], json.dumps({"intent": "write"})) for r in writes[:600]]
        + [chat(EXPLAIN_SYS, f"QUESTION: {r['sql_prompt']}\nSQL: {r['sql']}", r["sql_explanation"])
           for r in reads[2600:3400]])
random.seed(42)
random.shuffle(agent1)

for name, data in [("agent2_train.jsonl", agent2), ("agent1_train.jsonl", agent1)]:
    with open(f"finetune/{name}", "w", encoding="utf-8") as out:
        for example in data:
            out.write(json.dumps(example) + "\n")
print("Wrote", len(agent2), "Agent 2 examples and", len(agent1), "Agent 1 examples")