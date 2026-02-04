import matplotlib.pyplot as plt

sectors = ["Residential", "Commercial", "Industrial", "Agricultural","Government", "Hospitals", "Education", "Transport"]

consumption = [620, 480, 710, 560, 300, 1340, 290, 410]

plt.bar(sectors, consumption,edgecolor="black")
plt.xlabel("Sector")
plt.ylabel("Consumption")
plt.xlabel("Sectors")
plt.ylabel("Power Consumption (Million Units)")
plt.title("Electricity Consumption by Sector")
plt.xticks(rotation=10,fontsize =8)
plt.show()
