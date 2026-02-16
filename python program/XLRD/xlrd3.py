import xlrd
import matplotlib.pyplot as plt

filename = ("sales_data.xlsx")
openbook = xlrd.open_workbook(filename)
sheet = openbook.sheet_by_index(0)

print(sheet)
print(sheet.cell_value(0,2))

# print no of rows in sheet
print("Count of Rows",sheet.nrows)
print("Count of Cols:",sheet.ncols)

# bar graph product sales
# product = []
# product_sales = []

# product = []
# product[0] = 1
# print(product)

productdata = {}
# product1["name"] = "camera"
# print(product1)

for i in range(1,sheet.nrows):
    regionname = sheet.cell_value(i,2)
    producttotal = sheet.cell_value(i,9)

# check if key already exist or not
    if regionname in productdata:
         productdata[regionname] += producttotal
    else:
        productdata[regionname] = producttotal


print (productdata)

product_region = productdata.keys()
product_sales = productdata.values()

# create barr graph
plt.pie(product_sales,labels=product_region,autopct="%1.1f",colors=["lightgreen","aqua","gold","royalblue"])
plt.title("Product Sales")

plt.show()