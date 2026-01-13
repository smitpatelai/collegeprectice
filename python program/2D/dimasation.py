import numpy as np

data = np.array([
    [10,20,30],
    [40,50,60],
    [70,80,90]
])

print(data)

# access row and cols
print(data[0]) #row
print(data[:,0])

#element acces

print(data[1][2])
print(data[2][0])

#row slicing

print(data[:1])
print(data[1:])
