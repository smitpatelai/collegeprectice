import numpy as np

arry_1 = np.array([10, 20, 30, 40, 50])
ravel_arr = arry_1.ravel()

ravel_arr[0] = 200

print("Raveled array:", ravel_arr)
print("Original array:", arry_1)
