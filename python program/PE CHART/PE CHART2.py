import matplotlib.pyplot as plt


expense = {
    "Rent":2000,
    "Fuel":1500,
    "EMI":3500,
    "Food":7000,
    "Others":6000
}
explode = (0.05,0,0,0,0)
plt.pie(expense.values(),labels=expense.keys(),autopct="%1.1f",shadow=True,explode=explode)
plt.title("Expense of Individuals Employee at TCS")
plt.show()
