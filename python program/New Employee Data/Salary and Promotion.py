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
],dtype=object)
print(employee_data)
# print(employee_data.shape)
# Missing experience values (empty strings)
# Missing age values (empty strings)
# Invalid performance scores (zero or negative values)

np.savetxt("employee_details.csv", employee_data, delimiter=",", fmt="%s")
#load data form csv file

data = np.genfromtxt("employee_details.csv", delimiter=",", dtype=float, missing_values=np.nan, encoding="utf-8")
# print(data)
print("====================================================================================")
data[:,1] = np.where(np.isnan(data[:,1]),25,data[:,1])
data[:,2] = np.where(np.isnan(data[:,2]),8,data[:,2])

#remove negative from array data

data[:,3] = np.where(data[:,3]<=0,2,data[:,3])
data=data.astype(int)
print(data)

print(data.shape)
print("======================================================================================")
np.savetxt("employee_detail.csv", data, delimiter=",", fmt="%s")
print("======================================================================================")



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
np.savetxt("salary_details.csv", salary_data, delimiter=",", fmt="%s")

print("==================================================")
#load data form csv

#gemformtxt

sdata = np.genfromtxt("salary_details.csv", delimiter=",", missing_values=np.nan, dtype=float, encoding="utf-8")
# print(sdata)

#cleaning

#pprint 1st col data
# print(loaded_data[:,1])

#missing value at first col

sdata[:,1] = np.where(np.isnan(sdata[:,1]),25000, sdata[:,1])
sdata[:,2] = np.where(np.isnan(sdata[:,2]),2000, sdata[:,2])

# #remove negative from array data

sdata[:,1] = np.where(sdata[:,1]<=0,25000, sdata[:,1])
# print(loaded_data)
sdata=sdata.astype(int)
print(sdata)
print(sdata.shape)
#save this data in csv

np.savetxt("salary_detail.csv", sdata, delimiter=",", fmt="%s")
print("=====================================================================")


master_data = []

for emp in data:
    emp_id = emp[0]

    for sal in sdata:
        if emp_id == sal[0]:
            merged_row = np.concatenate((emp, sal[1:]))
            master_data.append(merged_row)

master_data = np.array(master_data)
master_data = master_data.astype(int)
print(master_data)
np.savetxt("master_data.csv", master_data, delimiter=",", fmt="%s")

