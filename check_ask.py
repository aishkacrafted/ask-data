from pipeline import ask

for q in ["How many orders were placed in 1997?",
          "Delete all orders from 1996",
          "Which 3 categories had the most revenue?"]:
    print("Q:", q)
    result = ask(q)
    print("A:", result["text"])
    if "data" in result:
        print(result["sql"])
        print(result["data"].head())
    print("-" * 50)