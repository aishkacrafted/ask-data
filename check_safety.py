from safety import validate

bad_queries = [
    "DROP TABLE orders",
    "DELETE FROM orders",
    "SELECT * FROM employees",
    "SELECT 1; SELECT 2",
    "SELECT pg_sleep(60)",
]

for sql in bad_queries:
    try:
        validate(sql)
        print("NOT BLOCKED:", sql)
    except ValueError as error:
        print("Blocked:", sql, "->", error)

print("Allowed:", validate("SELECT COUNT(*) FROM orders"))