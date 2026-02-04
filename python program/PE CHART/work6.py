import matplotlib.pyplot as plt

distance = [20, 40, 60, 80, 100, 120, 140, 160]
fuel = [2, 5, 9, 3, 17, 15, 18, 20]

plt.plot(distance, fuel, marker='o')
plt.xlabel("Distance Traveled (km)")
plt.ylabel("Fuel Used")
plt.title("Distance vs Fuel Used")
plt.grid(True)
plt.show()
