import numpy as np
import matplotlib.pyplot as plt

bar = np.zeros(shape=(40, 200, 3), dtype=np.uint8)

for progress in range(0, 200, 10):
    bar[:] = [20, 20, 20]        # Background (dark gray)
    bar[:, :progress] = [0, 240, 0]   # Green progress

    plt.imshow(bar)
    plt.axis("off")
    plt.title("Loading.....")
    plt.pause(0.3)
    plt.clf()
