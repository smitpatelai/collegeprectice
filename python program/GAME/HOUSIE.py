ticket = [5,12,89,54,36]
drawn = []

while True:
    number = int(input("Enter a number:"))
    if number not in drawn:
        drawn.append(number)

    guess = 0
    for i in ticket:
        if i in drawn:
            guess +=1
    print(f"YOu Have Guess {guess} / {len(ticket)}")

    choice=input("Do You Want to Continue? (y/n)")
    if choice=="y":
        pass
    elif choice=="n":
        print("You Have Quite the Game")
        break
    else:
        print("Invalid Choice")


    if guess == len(ticket):
        print("HOUSE!!!! YOU HAVE WON THE GAME")
        break

