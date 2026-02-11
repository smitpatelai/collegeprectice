import numpy as np
import matplotlib.pyplot as plt

# Create black square image
square = np.zeros((100, 100, 3), dtype=np.uint8)


# # method 1
# square[:, : ,0] = 255
# square[:,: ,1] = 0
# square[:, : ,2] = 0

# # method 2
# square[:] = [255,0,0]



# Dictionary of colors
colors = {
    "RED": [255, 0, 0],
    "GREEN": [0, 255, 0],
    "BLUE": [0, 0, 255],
    "PINK": [255, 103, 180],
    "BLUEVIOLET": [138,43,226]
}

# Show each color
for name, color in colors.items():
    square[:] = color
    plt.imshow(square)
    plt.title(name)
    plt.axis("off")
    plt.pause(0.5)
    plt.clf()
