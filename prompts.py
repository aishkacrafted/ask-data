SQL_SYS = ("You are a SQL generator. Output exactly one PostgreSQL SELECT query and nothing else. "     #Agent 2’s instruction
           "No explanations, no results, no comments, no markdown. Use only the tables given.")
#Agent 1’s two instructions
INTENT_SYS = "Decide whether the message asks to read data or change data. Reply in JSON."
EXPLAIN_SYS = "Explain in one or two plain sentences what this SQL query does."