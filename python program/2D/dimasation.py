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

# col slicing
print(data[:,1:])

#operations on array
print(data+3)

#reshape
arr_1 = np.array([1,2,3,4,5,6])
reshaped = arr_1.reshape(2,3)
print(reshaped)


flatten = data.flatten()
print(flatten)

#np.zeros

attendance = np.zeros((3,5), dtype=int)
print(attendance)
attendance[0][3] = 1
attendance[1][4] = 1
attendance[1][2] = 1
print(attendance)

salaries = np.array([
    [15000,2000,35000],# HR
    [15600,25000,36900],# TECh
    [10000,50000,60400] # SALES
])
print(salaries)

#print hr salary sum
sumofrow = np.sum(salaries,axis=1)
print(sumofrow[1])
print(sumofrow[2])

sumofcol = np.sum(salaries,axis=0)
print(sumofcol)

#print highest salary
print(np.max(salaries[:,2]))
