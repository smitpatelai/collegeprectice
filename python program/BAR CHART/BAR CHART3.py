import matplotlib.pyplot as plt

data = {
    "Clothes":150,
    "electronics":240,
    "Furniture":210
}

plt.bar(data.keys(),data.values())
plt.xlabel("Category")
plt.ylabel("Sales per hour")
plt.title("Sales of Various Categories(per hour)")
plt.show()
