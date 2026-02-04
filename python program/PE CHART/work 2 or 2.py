import matplotlib.pyplot as plt

expense_categories = ["Rent", "Food", "Transportation", "Utilities","Education", "Healthcare", "Entertainment", "Savings"]

expense_values = [30, 22, 10, 8, 12, 6, 7, 5]

explode = (0.05, 0, 0, 0, 0, 0, 0, 0)
plt.pie(expense_values,labels=expense_categories,autopct='%1.1f%%',shadow=True,explode=explode)
plt.title("Monthly Expense Distribution")
plt.legend(title="Expense Categories", loc="upper left", bbox_to_anchor=(0.91, 1.1))

plt.show()
