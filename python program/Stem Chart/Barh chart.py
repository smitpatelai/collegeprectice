import matplotlib.pyplot as plt

books = ["Mahabharat","Time Is Money","Avengers : Doomsday","The Hunter Game","Faith"]

sales = [2250,1020,1500,1150,350]

plt.figure(figsize=(12,6))
plt.barh(books,sales)
plt.yticks(fontsize=8)
plt.show()