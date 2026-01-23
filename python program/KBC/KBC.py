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

# data = load_question("KBC.txt")
# print(data)

def save_log(amount, duration):
    with open("kbc_price.txt","a") as file:
        file.write(f"QUIZ STARTED ON: {datetime.datetime.now()}\n")
        file.write(f"TOTAL AMOUNT WIN : {amount}\n")
        file.write(f"TOTAL DURATION: {duration}\n")

save_log(1000, 10)

def play_kbc():
    print("Welcome to KBC")
    question = load_question("KBC.txt")

    if len(question) == 0 :
        print("INVALID FILE")

    random.shuffle(question)
    totalamount = 0
    starttime = datetime.datetime.now()
    print(f"QUIZ STARTED AT: {starttime.strftime('%Y-%m-%d %H:%M:%S')}")

play_kbc()