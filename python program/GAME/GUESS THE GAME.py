def guess_game():
    numbers = [4,17,23,39,45,52,64,74,81,99]
    secret_no = 74
    chances = 3

    print("Walcome to Guess the Number Game")
    print(f"Number Are: {numbers}")
    print("You Have 3 Chances...")

    for i in range(1,chances+1):
        guess = int(input("Enter NO: "))

        if guess == secret_no:
            print("You Won!")
            break
        elif guess > secret_no:
            print("Too High!")
        elif guess < secret_no:
            print("Too Low!")
        else:
            print("Please Enter No From Given Data")
    print("You are Out of Attempts")

