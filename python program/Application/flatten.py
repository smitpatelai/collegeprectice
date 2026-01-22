import numpy as np

arry_1 = np.array([10, 20, 30, 40, 50])
flat_arr = arry_1.flatten()

flat_arr[0] = 100

print("Flattened array:", flat_arr)
print("Original array:", arry_1)
