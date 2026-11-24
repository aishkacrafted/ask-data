from db import run_query, log_question

print(run_query("SELECT COUNT(*) FROM orders"))

log_question("test", "read", "SELECT 1", 1, "ok", 0.1)
print("Logged a test row to audit_db")



