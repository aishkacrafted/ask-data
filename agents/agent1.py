from typing import Literal
from pydantic import BaseModel
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from prompts import INTENT_SYS, EXPLAIN_SYS

AGENT1_MODEL = "llama3.2:3b"  # replaced with the fine-tuned model later


class Intent(BaseModel):
    intent: Literal["read", "write"]


intent_prompt = ChatPromptTemplate.from_messages([("system", INTENT_SYS), ("human", "{message}")])
explain_prompt = ChatPromptTemplate.from_messages([
    ("system", EXPLAIN_SYS),
    ("human", "QUESTION: {question}\nSQL: {sql}"),
])

llm = ChatOllama(model=AGENT1_MODEL, temperature=0)
intent_chain = intent_prompt | llm.with_structured_output(Intent)
explain_chain = explain_prompt | llm | StrOutputParser()

if __name__ == "__main__":
    for m in ["How many orders were placed in 1997?", "Delete all orders from 1996",
              "Update the price of Chai to 20", "Which customers are in Germany?"]:
        print(m, "->", intent_chain.invoke({"message": m}).intent)
    print(explain_chain.invoke({"question": "How many orders in 1997?",
                                "sql": "SELECT COUNT(*) FROM orders WHERE EXTRACT(YEAR FROM order_date) = 1997;"}))