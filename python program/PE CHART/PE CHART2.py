import matplotlib.pyplot as plt


expense = {
    "Rent":2000,
    "Fuel":1500,
    "EMI":3500,
    "Food":7000,
    "Others":6000
}

plt.pie(expense.values(),labels=expense.keys(),autopct="%1.1f")
plt.title("Expense of Individuals Employee at TCS")
plt.show()
