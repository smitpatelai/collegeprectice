import pandas as pd

List_data = [20000,22000, 30000, 35000]

print(List_data)

data1 = pd. Series(List_data)
print(data1)

# component of series: index , data

# access elements of series
print(data1[2])

# create series using dict

dict = {
"Amit":15000,
"Jigar":20008,
"Anil":12000
}

data2 = pd. Series(dict)
print(data2)

# element access in dict - series
print(data2["Jigar"])

# operations in pandas
print(data2+3000)
print(max(data2))

# custom index in series

data3 = pd.Series( [101,102,103],index=["emp1","emp2","emp3"])
print(data3)
print(data3["emp3"])

# DATAFRAME
# components of dataframe
# row , col , data

# DATAFRAME USING LIST

list_Data1 = [
["Amit",12000,1],
["Jigar",15000,2],
["Anil",20000,1]
]

print(list_Data1[2][0])

df_list = pd.DataFrame(list_Data1)
print(df_list)

# access elements in dataframe
print(df_list[0] [2])

# dict_data1 = {
# "Amit": [12000,1],
# "Jigar": [15000,1],
# "Anil":[20000,2]
# }

dict_data1 = {
"Name": ["Amit","Jigar","Anil"],
"Salary": [12000,15000,10000],
"Exp": [1,2,1]
}

df_dict = pd.DataFrame(dict_data1)
print(df_dict)

print(df_dict["Salary"] [1])

# print all emp name -- access col
print(df_dict["Name"])
print("==============================")
# access row -- print 2nd row -- explore by yourself


print(df_dict.iloc[1])
