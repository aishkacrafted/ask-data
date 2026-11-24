import sqlglot
from sqlglot import exp

ALLOWED_TABLES = {"customers", "orders", "order_details", "products",
                  "categories", "suppliers", "shippers", "employees_public"}
FORBIDDEN = (exp.Insert, exp.Update, exp.Delete, exp.Drop, exp.Create, exp.Alter, exp.Command)    #commands that change data
BLOCKED_FUNCS = {"pg_sleep", "pg_read_file", "pg_ls_dir", "dblink", "set_config"} #freezes database


def validate(sql: str) -> str:
    sql = sql.replace("```sql", "").replace("```", "").strip()
    statements = sqlglot.parse(sql, read="postgres")
    if len(statements) != 1:
        raise ValueError("Exactly one statement allowed")
    tree = statements[0]
    if not isinstance(tree, (exp.Select, exp.Union)):
        raise ValueError("Only SELECT queries allowed")
    if any(True for _ in tree.find_all(*FORBIDDEN)):
        raise ValueError("Write or DDL operation detected")
    ctes = {c.alias_or_name for c in tree.find_all(exp.CTE)}
    used = {t.name for t in tree.find_all(exp.Table)} - ctes
    if not used <= ALLOWED_TABLES:
        raise ValueError(f"Unknown or forbidden tables: {used - ALLOWED_TABLES}")
    for fn in tree.find_all(exp.Anonymous):
        if fn.name.lower() in BLOCKED_FUNCS:
            raise ValueError(f"Function not allowed: {fn.name}")
    if isinstance(tree, exp.Select) and not tree.args.get("limit"):
        tree = tree.limit(1000)
    return tree.sql(dialect="postgres")


    #python check_safety.py