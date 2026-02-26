import pandas as pd

customers = pd. DataFrame({
"Customer_ID": [101, 102, 103, 104],
"Customer_Name": ["Amit", "Neha", "Raj", "Priya"],
"City": ["Mumbai", "Delhi", "Bangalore", "Pune"]
})
orders = pd. DataFrame({
"Order_ID": [1, 2, 3, 4, 5],
"Customer_ID": [101, 102, 101, 103, 105], # 105 does not exist in customers
"Product": ["Laptop", "Mobile", "Tablet", "Camera", "Headphones"],
"Amount": [50000, 20000, 30000, 25000, 5000]
})
payments = pd. DataFrame({
"Order_ID": [1, 2, 3, 6], # 6 does not exist in orders
"Payment_Method": ["UPI", "Card", "Cash", "Card"],
"Payment_Status": ["Success", "Success", "Pending", "Success"]
})
print("\n INNER JOIN -- CUSTOMER + ORDERS")
inner_join = pd.merge(customers, orders, on="Customer_ID",how="inner")
print(inner_join)

print("\n LEFT JOIN")
left_join = pd.merge(customers, orders, on="Customer_ID",how="left")
print(left_join)

print("\n RIGHT JOIN")
right_join = pd.merge(customers,orders,on="Customer_ID",how="right")
print(right_join)

print("\n OUTER JOIN")
outer_join = pd.merge(customers,orders, on="Customer_ID",how="outer")
print(outer_join)

print("\n ORDERS- PAYMENT PENDING")
data = pd.merge(orders,payments,on="Order_ID",how="left")
print(data)

print ("MASTER TABLE")
master = pd.merge(customers, orders, on="Customer_ID",how="left")
master = pd.merge(orders, payments, on="Order_ID",how="left")

print (master)

sales1 = pd.DataFrame({
"Product": ["Laptop","Mobile"],
"City": ["Mumbai","Delhi"],
"Sales":[12000,15000]
})
sales2 = pd.DataFrame({
"Product": ["Laptop", "Mobile"],
"City": ["Mumbai", "Delhi"],
"Target":[25000,30000]
})
multi_merge = pd.merge(sales1,sales2,on=["Product","City"],how="inner")
print(multi_merge)