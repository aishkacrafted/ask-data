To open venv: .venv\Scripts\activate

Baseline (llama3.1:8b, full schema in prompt): 10/20 = 50%
Wrong: (list the ids from baseline_output.txt)
Q20: wrong logic (COUNT(*) as 1996), wrong date column, ORDER BY on aliases (PostgreSQL error)

1 OK
2 OK
ERROR 3 Execution failed on sql 'SELECT COUNT(product_id) FROM products WHERE discontinued = TRUE LIMIT 1000': (psycopg.errors.UndefinedFunction) operator does not exist: integer = boolean
LINE 1: ...OUNT(product_id) FROM products WHERE discontinued = TRUE LIM...
                                                             ^
HINT:  No operator matches the given name and argument types. You might needto add explicit type casts.
[SQL: SELECT COUNT(product_id) FROM products WHERE discontinued = TRUE LIMIT1000]
(Background on this error at: https://sqlalche.me/e/21/f405)
3 WRONG
4 OK
5 OK
6 OK
7 OK
8 OK
9 WRONG
10 OK
11 OK
12 OK
13 WRONG
14 WRONG
15 WRONG
ERROR 16 Execution failed on sql 'SELECT c.category_name, SUM(od.quantity * od.unit_price * (1 - od.discount)) AS revenue FROM order_details AS od JOIN orders AS o ON od.order_id = o.order_id JOIN customers AS c ON o.customer_id =c.customer_id JOIN products AS p ON od.product_id = p.product_id JOIN categories AS cat ON p.category_id = cat.category_id WHERE EXTRACT(YEAR FROM o.order_date) = 1997 GROUP BY cat.category_name ORDER BY revenue DESC LIMIT 1000': (psycopg.errors.UndefinedColumn) column c.category_name does not exist
LINE 1: SELECT c.category_name, SUM(od.quantity * od.unit_price * (1...
               ^
HINT:  Perhaps you meant to reference the column "cat.category_name".
[SQL: SELECT c.category_name, SUM(od.quantity * od.unit_price * (1 - od.discount)) AS revenue FROM order_details AS od JOIN orders AS o ON od.order_id = o.order_id JOIN customers AS c ON o.customer_id = c.customer_id JOIN productsAS p ON od.product_id = p.product_id JOIN categories AS cat ON p.category_id= cat.category_id WHERE EXTRACT(YEAR FROM o.order_date) = 1997 GROUP BY cat.category_name ORDER BY revenue DESC LIMIT 1000]
(Background on this error at: https://sqlalche.me/e/21/f405)
16 WRONG
17 WRONG
C:\Users\001ho\OneDrive\Documents\code garam\ask-data\eval\run_eval.py:9: UserWarning: obj.round has no effect with datetime, timedelta, or period dtypes. Use obj.dt.round(...) instead.
  rows_a = sorted(a.round(2).astype(str).values.tolist())
18 WRONG
19 WRONG
ERROR 20 Execution failed on sql 'SELECT ship_country, COUNT(*) AS num_orders_1996, COUNT(CASE WHEN EXTRACT(YEAR FROM shipped_date) = 1997 THEN 1 END) ASnum_orders_1997 FROM orders GROUP BY ship_country ORDER BY num_orders_1997 -num_orders_1996 DESC LIMIT 1': (psycopg.errors.UndefinedColumn) column "num_orders_1997" does not exist
LINE 1: ...s_1997 FROM orders GROUP BY ship_country ORDER BY num_orders...
                                                             ^
[SQL: SELECT ship_country, COUNT(*) AS num_orders_1996, COUNT(CASE WHEN EXTRACT(YEAR FROM shipped_date) = 1997 THEN 1 END) AS num_orders_1997 FROM ordersGROUP BY ship_country ORDER BY num_orders_1997 - num_orders_1996 DESC LIMIT 1]
(Background on this error at: https://sqlalche.me/e/21/f405)
20 WRONG
Accuracy: 10/20 = 50%


[SQL: SELECT ship_country, COUNT(*) AS num_orders_1996, COUNT(CASE WHEN EXTRACT(YEAR FROM shipped_date) = 1997 THEN 1 END) AS num_orders_1997 FROM orders GROUP BY ship_country ORDER BY num_orders_1997 - num_orders_1996 DESC LIMIT 1]
(Background on this error at: https://sqlalche.me/e/21/f405)
20 WRONG
21 OK
22 OK
23 OK
24 OK
25 OK
26 OK
27 OK
28 OK
29 OK
30 WRONG
31 OK
32 WRONG
33 OK
34 WRONG
35 OK
36 WRONG
37 WRONG
38 WRONG
ERROR 39 Execution failed on sql 'SELECT (SUM(od.quantity * od.unit_price * (1 - od.discount)) FILTER(WHERE p.category_id = 1)) * 100 / (SELECT SUM(quantity * unit_price * (1 - discount)) FROM order_details AS od JOIN products AS p ON od.product_id = p.product_id) AS beverages_percentage FROM order_details AS od JOIN products AS p ON od.product_id = p.product_id WHERE p.category_id = 1 LIMIT 1000': (psycopg.errors.AmbiguousColumn) column reference "unit_price" is ambiguous
LINE 1: ....category_id = 1)) * 100 / (SELECT SUM(quantity * unit_price...
                                                             ^
[SQL: SELECT (SUM(od.quantity * od.unit_price * (1 - od.discount)) FILTER(WHERE p.category_id = 1)) * 100 / (SELECT SUM(quantity * unit_price * (1 - discount)) FROM order_details AS od JOIN products AS p ON od.product_id = p.product_id) AS beverages_percentage FROM order_details AS od JOIN products AS p ON od.product_id = p.product_id WHERE p.category_id = 1 LIMIT 1000]
(Background on this error at: https://sqlalche.me/e/21/f405)
39 WRONG
40 WRONG
Accuracy: 22/40 = 55%



Agent 1 intent accuracy: 23/30 = 77%