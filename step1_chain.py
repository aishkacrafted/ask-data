from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from prompts import SQL_SYS

# Decscribing the tables
SCHEMA = """            
customers(customer_id, company_name, contact_name, city, country)
orders(order_id, customer_id, employee_id, order_date, required_date, shipped_date, ship_via, freight, ship_city, ship_country)
order_details(order_id, product_id, unit_price, quantity, discount)
products(product_id, product_name, supplier_id, category_id, unit_price, units_in_stock, discontinued)
categories(category_id, category_name, description)
suppliers(supplier_id, company_name, city, country)
shippers(shipper_id, company_name, phone)
employees_public(employee_id, first_name, last_name, title, hire_date, city, country, reports_to)
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", SQL_SYS),
    ("human", "SCHEMA:\n{schema}\nREQUEST: {request}"),
])
llm = ChatOllama(model="llama3.1:8b", temperature=0) #same question always have same answer
sql_chain = prompt | llm | StrOutputParser()  

if __name__ == "__main__":
    for q in ["How many orders were placed in 1997?",
              "Top 5 products by quantity sold",
              "Which country has the most customers?"]:
        print(q)
        print(sql_chain.invoke({"schema": SCHEMA, "request": q}))
        print("-" * 40)

