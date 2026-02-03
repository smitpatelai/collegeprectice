import matplotlib.pyplot as plt

data ={
    "Category":["Furniture","Electronics","Clothes","Food","Medical"],
    "Sales":[150,210,260,290,400]
}

plt.bar(data["Category"],data["Sales"],color=["blue","red","yellow","green","black"])
plt.xlabel("Category")
plt.ylabel("Sales")
plt.title("Sales of Various Categories")
plt.xticks(rotation=90)
plt.show()
