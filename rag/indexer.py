import json
import yaml
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

emb = OllamaEmbeddings(model="nomic-embed-text")


def store(name):
    return Chroma(collection_name=name, embedding_function=emb, persist_directory="vectordb")


knowledge = yaml.safe_load(open("rag/knowledge.yaml", encoding="utf-8"))

tables = store("tables")
tables.add_documents(
    [Document(page_content=f"Table {t['name']}: {t['description']} Columns: {t['columns']}",
              metadata={"table": t["name"]})
     for t in knowledge["tables"]],
    ids=[t["name"] for t in knowledge["tables"]],
)

glossary = store("glossary")
glossary.add_documents(
    [Document(page_content=f"{g['term']}: {g['meaning']}") for g in knowledge["glossary"]],
    ids=[g["term"] for g in knowledge["glossary"]],
)

examples = [json.loads(line) for line in open("rag/examples.jsonl", encoding="utf-8") if line.strip()]
example_store = store("examples")
example_store.add_documents(
    [Document(page_content=e["question"], metadata={"sql": e["sql"]}) for e in examples],
    ids=[f"ex{i}" for i in range(len(examples))],
)

print("Indexed", len(tables.get()["ids"]), "tables,",
      len(glossary.get()["ids"]), "glossary terms,",
      len(example_store.get()["ids"]), "examples")

print("\nTest search: 'units sold per product in 1997'")
for doc in tables.similarity_search("units sold per product in 1997", k=4):
    print("-", doc.metadata["table"])