import matplotlib.pyplot as plt

category = ["Furniture","Electronics","Clothes","Food","Medical"]
sale =[150,210,260,290,400]

plt.bar(category,sale)
plt.xlabel("Category")
plt.ylabel("Sales")
plt.title("Sales of Different Category")
plt.xticks(category)
plt.yticks(sale)
plt.show()
