import matplotlib.pyplot as plt

appliances = ["Air Conditioner","Refrigerator","Lighting","Washing Machine","Television","Kitchen Appliances"]

energy = [28, 30, 15, 12, 10, 17]

plt.bar(appliances, energy)
plt.xlabel("Appliances")
plt.ylabel("Energy Consumption")
plt.xticks(rotation=15,fontsize =9)
plt.title("Household Energy Consumption Breakdown")
plt.show()
