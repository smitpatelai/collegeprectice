import numpy as np

list_1 = [10,20,30]
list_2 = [30,40,50]
merged_list = list_1 + list_2


# method 1
for i in list_1:
    print(i)

# method 2

for i in range(len(list_1)):
    merged_list.append(list_1[i]+list_2[i])


#print(merged_list)

#----using numpy3

#list to array

arr_1 = np.array(list_1)
arr_2 = np.array(list_2)
merged_array = arr_1 + arr_2

print(merged_array)


marks_list = [70,60,93,88,64]

total = 0

for i in range(len(marks_list)):
    total += marks_list[i]

print (total)
marks_mean = total/len(marks_list)
print(marks_mean)

marks_array = np.array(marks_list)
print("marks mean using numpy",marks_array.mean())


#NUMPY ARRAY CREATION

arr_arange = np.arange(1,10)
print(arr_arange)

arr_zero = np.zeros(5,dtype=int)
print(arr_zero)

arr_ones = np.ones(5,dtype=int)
print(arr_ones)

arr_data = np.arange(1,100)
print(arr_data)

#accessing elements

print(arr_data[3])
print(arr_data[5:10])


#Operations

print("Update marks", marks_array+5)
print(marks_array+2)

#method

print("mean",marks_array.mean())
print("max marks",marks_array.max())
print("min marks",marks_array.min())
print("sum",marks_array.sum())
print(marks_array.argmax())
print(marks_array.argmin())

