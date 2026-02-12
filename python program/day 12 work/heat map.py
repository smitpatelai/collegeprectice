import numpy as np
import matplotlib.pyplot as plt

data = np.random.randint(0, 256, (60, 80, 3))

print("Shape:", data.shape)
np.save("raw_traffic_data.npy", data)
data = np.load("raw_traffic_data.npy")
data[data < 5] = 0
data[data > 240] = 240

print("Min:", data.min())
print("Max:", data.max())
total = np.sum(data, axis=2)
plt.imshow(total, cmap="PuBuGn")
plt.title("Website Heatmap")
plt.show()

z1 = np.sum(total[:30, :40])
z2 = np.sum(total[:30, 40:])
z3 = np.sum(total[30:, :40])
z4 = np.sum(total[30:, 40:])

print("Top-Left:", z1)
print("Top-Right:", z2)
print("Bottom-Left:", z3)
print("Bottom-Right:", z4)
