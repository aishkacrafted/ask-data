CREATE ROLE ai_reader LOGIN PASSWORD 'reader_pw'; --a login just for the AI
GRANT CONNECT ON DATABASE northwind TO ai_reader;
GRANT USAGE ON SCHEMA public TO ai_reader;

CREATE VIEW employees_public AS
  SELECT employee_id, first_name, last_name, title, hire_date, city, country, reports_to
  FROM employees;

GRANT SELECT ON customers, orders, order_details, products, categories,
                suppliers, shippers, employees_public TO ai_reader; --only reads these 8 tables

ALTER ROLE ai_reader SET default_transaction_read_only = on; --lock for read only
ALTER ROLE ai_reader SET statement_timeout = '15s';