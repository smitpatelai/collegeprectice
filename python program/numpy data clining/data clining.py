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

loaded_data[:,1] = np.where(loaded_data[:,1]<0,90000, loaded_data[:,1])
print(loaded_data)

print(loaded_data.shape)



# convert loaded_data into int

loaded_data = loaded_data.astype(int)
print(loaded_data)

#store this data into final file
# np.savetxt("finalsalarydata.csv", loaded_data, delimiter=",", fmt="%s")

#find employee who has highest salary
#find avg salary
#find employee who have salary between 12500- 14500
#total salary
#store all data according to salary in csv file

print(np.max(loaded_data))
print("======================================")
print(np.average(loaded_data))
print("AVG SALARY")
print("======================================")
print("Total salary")
print(np.sum(loaded_data))
print("======================================")

# salary_range = loaded_data[(loaded_data[:,1] >= 12500) & (loaded_data[:,1] <= 14500)]
#
# print("Employees with salary between 12500 and 14500:\n", salary_range)

salary_range_emp = loaded_data[(loaded_data[:, 1] >= 11500) & (loaded_data[:, 1] <= 13000)]
print(salary_range_emp)

# sort by salary (2nd column)
sorted_data = loaded_data[loaded_data[:,1].argsort()]

# save to CSV
np.savetxt(
    "salary_sorted.csv",
    sorted_data,
    delimiter=",",
    fmt="%d",
    header="EmpID,Salary,Dept",
    comments=""
)

print("Data saved to salary_sorted.csv")



student_data = np.array([
    [1,78,3],
    [2,"",2],
    [3,105,1],
    [4,-5,""],
    [5,66,2],
    [6,None,1],
    [7,45,0],
    [8,89,3]
], dtype=object)

#store data into csv file
#load data from csv file
#clean data
# 1. marks can not be none , null and less than zero and greater than 100
# 2. status can not be blank , none, greater than 1
        # 35>--- pass status = 1
        # 35<--- pass status =0
#store final result into different student file to pass status


np.savetxt("student_data.csv",student_data,delimiter=",",fmt="%s")

loaded_data = np.genfromtxt("student_data.csv",delimiter=",",dtype=object,encoding="utf-8")

# print(loaded_data)
marks = loaded_data[:,1]

clean_marks = []
for m in marks:
    try:
        m = int(m)
        if m < 0 or m > 100:
            clean_marks.append(0)
        else:
            clean_marks.append(m)
    except:
        clean_marks.append(0)

loaded_data[:,1] = clean_marks

marks = loaded_data[:,1].astype(int)

status = np.where(marks >= 35, 1, 0)
loaded_data[:,2] = status


final_data = loaded_data.astype(int)
print("Final Cleaned Data:\n", final_data)

pass_students = final_data[final_data[:,2] == 1]

np.savetxt("pass_students.csv",pass_students,delimiter=",",fmt="%d",header="ID,Marks,Status",comments="")

fail_students = final_data[final_data[:,2] == 0]

np.savetxt("fail_students.csv",fail_students,delimiter=",",fmt="%d",header="ID,Marks,Status",comments="")

