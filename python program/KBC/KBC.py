import datetime
import random
import math

def load_question(filename):
    question = []
    with open(filename,"r",encoding="utf-8") as file:
        lines = [line.strip() for line in file if line.strip()]
        for i in range(0, len(lines),7):
            if i + 6 < len(lines):
                question.append({
                    "question": lines[i],
                    "options": lines[i+1:5],
                    "answer": int(lines[i+5]),
                    "money": int(lines[i+6])
                })

        return question

data = load_question("KBC.txt")
print(data)
