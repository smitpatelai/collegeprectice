import matplotlib.pyplot as plt

x = [10, 40, 30, 50, 60, 20, 70, 90, 80]
y = [1, 2, 3, 4, 5, 6, 7, 8, 9]

while True:
    print("\nAvailable charts")
    print("line")
    print("bar")
    print("scatter")
    print("hist")
    print("pie")

    choice = input("Which chart you want to make: ").lower()

    if choice == "line":
        plt.plot(y, x)
        plt.show()
        break

    elif choice == "bar":
        plt.bar(y, x)
        plt.show()
        break

    elif choice == "scatter":
        plt.scatter(y, x)
        plt.show()
        break

    elif choice == "hist":
        plt.hist(x)
        plt.show()
        break

    elif choice == "pie":
        plt.pie(x, labels=y)
        plt.show()
        break

    else:
        print("Invalid Input")
        break

plt.show()