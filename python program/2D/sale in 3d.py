import numpy as np


sales = np.array([
                    [[10, 20, 30], [15, 25, 35]],
                    [[12, 22, 32], [18, 28, 38]],
                    [[14, 24, 34], [20, 30, 40]],
                    [[16, 26, 36], [22, 32, 42]],
                    [[18, 28, 38], [24, 34, 44]],
                    [[20, 30, 40], [26, 36, 46]],
                    [[22, 32, 42], [28, 38, 48]]
])

# block > Day (7 days)
# ROW [ 2 ] > Shift (Morning, Evening)
# COL [ 3 ] > Product (P1, P2, P3)

# TASK
#1 Print the shape of the sales array
#2 Explain what each dimension represents
#3 Print sales data of Day 3
#4 Print evening shift sales for all days
#5 Print sales of Product 2 for all days and shifts
#6 Print sales of Product 1 on Day 1 Morning shift

#7 A sale below 25 units is considered low
# Tasks:
        # Use masking to find all low-sale values
        # Count total number of low-sale entries

#8 Calculate total sales per day
#9 Calculate total sales per shift
#10 Calculate total sales per product

# 11 Identify the day with highest total sales
# 12 Identify the product with lowest overall sales

# 1 for print array
print(sales)
print("===============")
# 2 for print shape
print(sales.shape)
print("=============")
#3
print(sales[2])
#4
print("=======================")
print(sales[:,2-1])
print("============OR============")
print(sales[0:7,1:2,0:3])
print("==========================")
#5
print(sales[0:7,0:3,1:2])
print("=======================")
#6
print(sales[0:1,0:1,0:1])
print("===========OR=========")
print(sales[0,0,0])
print("============================")
#7
arr = sales[sales[0:7,0:2,0:3]<25]
print(f"LOW VALUE OF PRODUCT (UNDER 25) IS :\n {arr}")

print(arr.sum(axis=0))
print("===================OR=============")
print(sales[sales< 25])
print("========OR==========")
print(sales[sales[0:7,0:2,0:3]<25])
print("===============================")
#8
print(sales.sum(axis=(1,2)))
print("==========OR=========")
total_sales_per_day = np.sum(sales, axis=(1, 2))
print(total_sales_per_day)
print("================================")
#9
print(sales.sum(axis=(0,2)))
print("================================")
#10
print(sales.sum(axis=(1,2,0)))
print("==============================")
#11
