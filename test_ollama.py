import ollama

models = ollama.list()
for m in models:
    name = m[0]      # numele modelului
    size = m[1]      # dimensiunea modelului
    print(f"Name: {m[0]} Size: {m[1]}\n")