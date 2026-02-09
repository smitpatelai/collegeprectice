import matplotlib.pyplot as plt

x = [10, 40, 30, 50, 60, 20, 70, 90, 80]
y = [1, 2, 3, 4, 5, 6, 7, 8, 9]

print("\nAvailable charts")
print("line")
print("bar")
print("scatter")
print("hist")
print("pie")

choice = input("Which chart you want to make: ").lower()
if choice == "line" or choice == "linechart":
    plt.plot(y, x)

elif choice == "bar" or choice == "barchart":
    plt.bar(y, x)

elif choice == "scatter":
    plt.scatter(y, x)

elif choice == "hist" or choice == "histogram" or choice == "histo":
    plt.hist(y)

elif choice == "pie" or choice == "piechart":
    plt.pie(x, labels=y)

else:
    print("Invalid Input")

plt.show()
