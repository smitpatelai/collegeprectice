import matplotlib.pyplot as plt

months = ["Jan", "Feb", "Mar", "Apr", "May"]

social = [1200, 100, 50000, 15000, 600]
ads = [1800, 9000, 10000, 1100, 12000]
organic = [21000, 12100, 52900, 62300, 32400]

plt.plot(months, social, marker='o', label='Social')
plt.plot(months, ads, marker='+', label='Ads')
plt.plot(months, organic, marker='*', label='Organic')

plt.title("Marketing Performance (Jan–May)")
plt.xlabel("Months")
plt.ylabel("Leads / Traffic")
plt.legend()
plt.grid(True)

plt.show()
