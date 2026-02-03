import colorama
import matplotlib.pyplot as plt


expense = {
    "Rent":2000,
    "Fuel":1500,
    "EMI":3500,
    "Food":7000,
    "Others":6000
}
explode = (0.05,0,0,0,0)
colors = ("tan","olive","darkslateblue","royalblue","slategray")
plt.pie(expense.values(),labels=expense.keys(),autopct="%1.1f",colors=colors,shadow=True,explode=explode)
plt.title("Expense of Individuals Employee at TCS")
plt.legend(title="Expanse Name",loc="center right",bbox_to_anchor=(1.1,1.1))
plt.show()
