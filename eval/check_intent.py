import json
from agents.agent1 import intent_chain

correct = total = 0
for line in open("eval/intent_messages.jsonl", encoding="utf-8"):
    if not line.strip():
        continue
    m = json.loads(line)
    total += 1
    try:
        got = intent_chain.invoke({"message": m["message"]}).intent
    except Exception as error:
        got = f"error: {error}"
    ok = got == m["intent"]
    correct += ok
    if not ok:
        print("WRONG:", m["message"], "| expected", m["intent"], "| got", got)
print(f"Agent 1 intent accuracy: {correct}/{total} = {correct / total:.0%}")