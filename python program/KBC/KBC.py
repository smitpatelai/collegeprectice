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
                    "options": lines[i+1:i+5],
                    "answer": int(lines[i+5]),
                    "money": int(lines[i+6])
                })

        return question

data = load_question("KBC.txt")
print(data)

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

    max_question = min(15, len(question))

    for i in range(max_question):
        q = question[i]

        print(f"question: {i+1} | AMOUNT : {q['money']}")
        print(f"{q['question']}")

        for idx , b in enumerate(q["options"]):
            print(f"{idx+1} |  {b}")

        try:
            chooice = int(input("Enter Choice In No(1-4): "))
        except ValueError:
            print("GAME OVER!!!!!!! Invalid Option or Answer")
            break

        if chooice == q["answer"]:
            totalamount += q["money"]
            bonus = int(math.sqrt(q["money"]))
            print("Correct Answer")
            print(f"BONUS POINTS: {bonus}")
            print(f"Total Amount: {totalamount}")
        else:
            print("Game Over")
            print(f"Current Amount: {totalamount}")
            break

    end_time = datetime.datetime.now()
    duration = end_time - starttime
    print("Game Over")
    print(f"Game Ended at:{end_time}")
    print(f"Total Duration: {duration}")

    save_log(totalamount, duration)

play_kbc()