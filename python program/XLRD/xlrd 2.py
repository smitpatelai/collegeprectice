import xlrd
import matplotlib.pyplot as plt

filename = ("sales_data.xlsx")
openbook = xlrd.open_workbook(filename)
sheet = openbook. sheet_by_index(0)

dates = []
sales =[]

for i in range(1,10):
    dates.append(sheet.cell_value(i,1))
    sales.append(int(sheet.cell_value(i,9)))

print(dates)
print(sales)

plt.plot(dates,sales)
plt.xlabel ("Dates")
plt.ylabel("Sales")
plt.title("Trend of Sales")
plt.show()
