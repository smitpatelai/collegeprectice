import matplotlib.pyplot as plt

x = [10, 40, 30, 250, 160, 120, 370, 90, 80]
y = [1, 2, 3, 4, 5, 6, 7, 8, 9]
a = [x,y]
while True:
    print("\nAvailable charts")
    print("line")
    print("bar")
    print("scatter")
    print("hist")
    print("pie")
    print("violin")
    print("barh")

    choice = input("Which chart you want to make: ").lower()
    color = input("Enter color (e.g. aquamarine, crimson, gold, olive): ").lower()

    if choice == "line":
        plt.plot(y, x,color=color)
        plt.show()
        break

    elif choice == "bar":
        plt.bar(y, x,color=color)
        plt.show()
        break

    elif choice == "scatter":
        plt.scatter(y, x,color=color)
        plt.show()
        break

    elif choice == "hist":
        plt.hist(x,color=color)
        plt.show()
        break

    elif choice == "pie":
        plt.pie(x, labels=y,color=color)
        plt.show()
        break

    elif choice == "violin":
        plt.violinplot(a)
        plt.show()
        break

    elif choice == "barh":
        plt.barh(y, x,color=color)
        plt.show()
        break

    else:
        print("Invalid Input ❌ Try again")
