import matplotlib.pyplot as plt

expense_categories = ["Rent", "Food", "Transportation", "Utilities","Education", "Healthcare", "Entertainment", "Savings"]

expense_values = [30, 22, 10, 8, 12, 6, 7, 5]

plt.pie(expense_values,labels=expense_categories,autopct='%1.1f%%',startangle=90)

plt.title("Household Monthly Expense Distribution")

plt.axis('equal')

plt.show()
