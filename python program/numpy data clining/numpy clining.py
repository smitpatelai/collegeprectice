import numpy as np
import time

report = np.array([
    [101,25000,1],
    [102,32000,2],
    [103,28000,3],
    [104,40000,4],
    [105,24000,1],
    [106,20000,2],
])


#cache

#store this data into binary file
# np.save("hrreport.txt", report)
#
#
#
# #load data from binary file
#
# loaded_report = np.load("hrreport.txt")
# print(loaded_report)
#

# copy vs view

# view_data = loaded_report[:3]
# # print(view_data)
#
# copy_data = loaded_report[3:].copy()
# print(view_data)

# view_data[1,1] = 10000
# print(view_data)
#
# copy_data[1,1] = 9999
# print(view_data)


# salary_data = np.random.randint(20000,40000,size=1000000000)

#total expenses
#
# starttime = time.time()
# totalsum_loop = 0
# for i in salary_data:
#     totalsum_loop+=i
#
# endtime = time.time()
#
# print("total time consumed by loop: ",endtime-starttime)

#total expenses using numpy
#
# starttime1 = time.time()
#
# totalsum_numpy = np.sum(salary_data)
#
# endtime1 = time.time()

# print("total time consumed by numpy: ",endtime1-starttime1)


#BROADCASTING
#
# emp_data = np.array([
#     [10000,12000,15000],
#     [20000,22000,25000],
# ])
#
# print(emp_data)
# print(emp_data.shape)


#monthly
#
# bonus = np.array([
#     [10000,12000,15000],
# ])
#
# print(bonus)
# print(bonus.shape)
#
# emp_data = emp_data + bonus
# print(emp_data)
#
# tax = np.array([
#     [1000],
#     [1300],
# ])
#
# updateslary = emp_data-tax
# print(updateslary)




#task:

emp_data = np.array([
    [101,30000,6],
    [102,28000,8],
    [103,35000,9],
    [104,26000,5],
    [105,40000,10]
])

#store data into csv
#mask data

      #performance > 7 ----> give bonus 5000
      #make copy
      #apply changes in copy

#store data in csv
#do this with np.where and broadcasting

# 1. Store original data into CSV

np.savetxt("emp_data.csv",emp_data,delimiter=",",fmt="%d",comments="")

# 2. Mask: performance > 7

mask = emp_data[:, 2] > 5

# 3. Make a copy

emp_bonus = emp_data.copy()

# 4. Apply bonus using np.where & broadcasting
#    Bonus = 5000 if performance > 7

emp_bonus[:, 1] = np.where(mask,emp_bonus[:, 1] + 9000,emp_bonus[:, 1])

# 5. Store updated data into CSV

np.savetxt("emp_bonus_data.csv",emp_bonus,delimiter=",",fmt="%d",comments="")

# 6. Output check

print("Original Data:\n", emp_data)
print("\nBonus Applied Data:\n", emp_bonus)



#new without np.where useing

emp_copy = emp_data.copy()

mask = emp_copy[:, 2] > 5

emp_copy[mask, 1]+=45000

print(emp_copy)