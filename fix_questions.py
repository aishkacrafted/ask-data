import json

path = "eval/questions.jsonl"
text = open(path, encoding="utf-8-sig").read()
decoder = json.JSONDecoder()
questions, i = [], 0
while True:
    i = text.find("{", i)
    if i == -1:
        break
    obj, i = decoder.raw_decode(text, i)
    questions.append(obj)

with open(path, "w", encoding="utf-8") as out:
    for q in questions:
        out.write(json.dumps(q) + "\n")
print(f"Fixed: {len(questions)} questions, one per line")