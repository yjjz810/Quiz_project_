import json
with open("question.json","r",encoding="UTF-8") as file:
    question=json.load(file)

print(question)