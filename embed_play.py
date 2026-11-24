import numpy as np
from langchain_ollama import OllamaEmbeddings

emb = OllamaEmbeddings(model="nomic-embed-text")
sentences = ["total sales per month", "monthly revenue", "number of employees",
             "staff headcount", "best selling product", "weather in Edmonton"]
v = np.array(emb.embed_documents(sentences))
v = v / np.linalg.norm(v, axis=1, keepdims=True)
for sentence, row in zip(sentences, v @ v.T):
    print(f"{sentence:25}", " ".join(f"{x:.2f}" for x in row))