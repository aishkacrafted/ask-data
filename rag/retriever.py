from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_community.utilities import SQLDatabase
from db import READER_URL
from safety import ALLOWED_TABLES

emb = OllamaEmbeddings(model="nomic-embed-text")
tables = Chroma(collection_name="tables", embedding_function=emb, persist_directory="vectordb")
glossary = Chroma(collection_name="glossary", embedding_function=emb, persist_directory="vectordb")
examples = Chroma(collection_name="examples", embedding_function=emb, persist_directory="vectordb")
db = SQLDatabase.from_uri(READER_URL, include_tables=sorted(ALLOWED_TABLES),
                          view_support=True, sample_rows_in_table_info=2)

JOINS = {
    "orders": ["customers", "order_details"],
    "order_details": ["orders", "products"],
    "products": ["categories", "suppliers"],
}


def retrieve(question):
    names = {d.metadata["table"] for d in tables.similarity_search(question, k=4)}
    for name in list(names):
        names |= set(JOINS.get(name, []))
    names &= ALLOWED_TABLES
    schema = db.get_table_info(table_names=sorted(names))
    terms = "\n".join(d.page_content for d in glossary.similarity_search(question, k=3))
    shots = "\n\n".join(f"Q: {d.page_content}\nSQL: {d.metadata['sql']}"
                        for d in examples.similarity_search(question, k=3))
    return names, f"{schema}\n\nGLOSSARY:\n{terms}\n\nEXAMPLES:\n{shots}"


if __name__ == "__main__":
    names, context = retrieve("units sold per product in 1997")
    print("Tables:", sorted(names))
    print(context[:1500])