import re
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from prompts import SQL_SYS

AGENT2_MODEL = "llama3.1:8b"  # replaced with the fine-tuned model later


def extract_sql(text):
    text = text.replace("```sql", "").replace("```", "")
    match = re.search(r"\b(SELECT|WITH)\b.*?(;|$)", text, re.IGNORECASE | re.DOTALL)
    return match.group(0).strip() if match else text.strip()


prompt = ChatPromptTemplate.from_messages([
    ("system", SQL_SYS),
    ("human", "SCHEMA:\n{schema}\nREQUEST: {request}"),
])
llm = ChatOllama(model=AGENT2_MODEL, temperature=0)
sql_chain = prompt | llm | StrOutputParser() | extract_sql