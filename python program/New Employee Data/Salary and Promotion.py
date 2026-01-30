import numpy as np

employee_data = np.array([
    [101, 25, 2, 7, 1],
    [102, 30, 3, 8, 2],
    [103, 28, '', 6, 1],
    [104, '', 5, 9, 3],
    [105, 35, 7, 10, 2],
    [106, 26, 1, 0, 1],
    [107, 40, 10, 8, 3],
    [108, 29, '', 5, 2],
    [109, 33, 4, 7, 1],
    [110, 27, 2, -1, 2]
])
# print(employee_data)

print(employee_data.shape)
# Missing experience values (empty strings)
# Missing age values (empty strings)
# Invalid performance scores (zero or negative values)

np.savetxt("employee_details.csv", employee_data, delimiter=",", fmt="%s")

#load data form csv file

data = np.loadtxt("employee_details.csv", delimiter=",", dtype=object, encoding="utf-8")
print(data)
print("====================================================================================")

salary_data = np.array([
    [101, 25000, 2000, 3000, 1000],
    [102, 32000, 3000, 4000, 2000],
    [103, '', 2500, 3500, 1500],
    [104, 40000, 4000, 5000, 3000],
    [105, -1, 5000, 6000, 2500],
    [106, 28000, '', 3000, 1200],
    [107, 45000, 6000, 7000, 3500],
    [108, 30000, 2000, 4000, 1800],
    [109, '', 3000, 3500, 1500],
    [110, 26000, 1500, 2500, 1000]
],dtype=object)
print("=====================================================================================")
print(salary_data)

#save this data in csv

np.savetxt("salary_details.csv", salary_data, delimiter=",", fmt="%s")

#load data form csv

#gemformtxt

loaded_data = np.genfromtxt("salary_details.csv", delimiter=",", filling_values=np.nan, dtype=float)
# print(loaded_data)

#cleaning

#pprint 1st col data
# print(loaded_data[:,1])

#missing value at first col

loaded_data[:,1] = np.where(np.isnan(loaded_data[:,1]),100, loaded_data[:,1])
loaded_data[:,2] = np.where(np.isnan(loaded_data[:,2]),10, loaded_data[:,2])

#remove negative from array data

loaded_data[:,1] = np.where(loaded_data[:,1]<0,10, loaded_data[:,1])
# print(loaded_data)

print(loaded_data.shape)
