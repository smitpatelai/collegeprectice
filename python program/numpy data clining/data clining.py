import numpy as np

#DATA CLEANING

emp_data = np.array([
    [101,12000,3],
    [102,12600,1],
    [103,13000,1],
    [104,-1,2],
    [105,14000,2],
    [106,1500,1],
    [107,1600,1],
    [108,1700,1],
])

print(emp_data)
print(emp_data.shape)

#ID OPREATINGS
#SAVE THIS DATA INTO FILE
np.savetxt("emp_data.csv", emp_data, delimiter=",", fmt="%d")

#load data form csv file

data = np.loadtxt("emp_data.csv", delimiter=",", dtype=int)
print(data)

#know the difference of rang for all data types
#genformtxt

salary_data = np.array([
    [101,'',3],
    [102,12600,1],
    [130,12000,1],
    [140,-1,2],
    [150,14000,''],
    [160,15000,2],
    [170,16000,1],
    [180,17000,2],
],dtype=object)

print(salary_data)

#save this data in csv

np.savetxt("salary_data.csv", salary_data, delimiter=",", fmt="%s")

#load data form csv

#gemformtxt

loaded_data = np.genfromtxt("salary_data.csv", delimiter=",",filling_values=np.nan,dtype=float)
print(loaded_data)


#cleaning

#pprint 1st col data
print(loaded_data[:,1])

#missing value at first col

loaded_data[:,1] = np.where(np.isnan(loaded_data[:,1]),10000, loaded_data[:,1])
loaded_data[:,2] = np.where(np.isnan(loaded_data[:,2]),10, loaded_data[:,2])

#remove negative from array data

loaded_data = np.where(loaded_data[:,1]<0,90000, loaded_data[:,1])
print(loaded_data)

# convert loaded_data into int

loaded_data = loaded_data.astype(int)
print(loaded_data)

#store this data into final file
np.savetxt("finalsalarydata.csv", loaded_data, delimiter=",", fmt="%s")

