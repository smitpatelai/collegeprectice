import random

# 0-1
print("Random N0 (0-1)",random.random())
#range(10-50)
print("Random no(10-50)",random.randint(10,50))
#float
print("Random Float No(10-50)",random.uniform(10,50))
#list
fruits = ["apple", "banana", "cherry"]
#random --> one
print("Random Data From List",random.choice(fruits))
#number
no = [10,20,30,40,50]
random.shuffle(no)
print("Random Data From List",no)
# 3 data
print("Now List:",random.sample(no,5))
