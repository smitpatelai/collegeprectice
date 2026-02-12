import numpy as np
import matplotlib.pyplot as plt

board = np.ones((8, 8))

for i in range(8):
    for j in range(8):
        if (i + j) % 2 == 0:
            board[i, j] = 0

plt.imshow(board, cmap="gray")
plt.xticks([])
plt.yticks([])
plt.title("Chess Board")
plt.show()
