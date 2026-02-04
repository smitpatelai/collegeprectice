import matplotlib.pyplot as plt

months = ["Jan", "Feb", "Mar", "Apr", "May"]

Rent = [1200, 100, 50000, 15000, 600]
Food = [1800, 9000, 10000, 1100, 12000]
Transportation = [21000, 12100, 52900, 62300, 32400]
Utilities = [200, 500, 100, 320, 130]
Education = [37000, 0, 120, 0, 37000]
Healthcare = [200, 100, 350, 250, 240]
Entertainment = [200, 100, 350, 250, 240]
Saving = [1200, 2100, 1350, 2250, 1240]

plt.plot(months, Rent, marker='o', label='Rent')
plt.plot(months, Food, marker='+', label='Food')
plt.plot(months, Transportation, marker='*', label='Transportation')
plt.plot(months, Utilities, marker='^', label='Utilities')
plt.plot(months, Education, marker='v', label='Education')
plt.plot(months, Healthcare, marker='D', label='Healthcare')     # fixed
plt.plot(months, Entertainment, marker='x', label='Entertainment') # fixed
plt.plot(months, Saving, marker='s', label='Saving')

plt.title("Monthly Household Expenses (Jan–May)")
plt.xlabel("Months")
plt.ylabel("Amount")
plt.legend()
plt.grid(True)

plt.show()
