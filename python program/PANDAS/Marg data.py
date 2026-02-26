import pandas as pd
# 1. Product Inventory
inventory = pd.DataFrame({
    "SKU": ["A101", "B202", "C303", "D404", "E505"],
    "Product_Name": ["Gaming Mouse", "Mechanical Keyboard", "Webcam", "Ring Light", "USB Hub"],
    "Stock_Level": [50, 20, 15, 0, 100],
    "Warehouse_ID": [1, 2, 1, 3, 2]
})

# 2. Sales Transactions
sales = pd.DataFrame({
    "Transaction_ID": [1001, 1002, 1003, 1004],
    "SKU": ["A101", "C303", "Z999", "A101"], # Note: Z999 is a mystery item
    "Quantity_Sold": [2, 1, 5, 1],
    "Sale_Date": ["2024-01-01", "2024-01-02", "2024-01-02", "2024-01-03"]
})

# 3. Warehouse Locations (Joining on Warehouse_ID)
warehouses = pd.DataFrame({
    "Warehouse_ID": [1, 2, 4], # Note: Warehouse 3 is missing here
    "Location": ["New York", "London", "Tokyo"],
    "Manager": ["Alice", "Bob", "Charlie"]
})

#Generate a list showing every Product_Name alongside how many units were sold (Quantity_Sold).
merged = pd.merge(inventory, sales, on="SKU", how="left")
print(merged)

#List all sales transactions, ensuring the Product_Name is visible for each SKU sold.
# Merge sales with inventory to get Product_Name
sales_with_product = pd.merge(inventory,sales,on="SKU",how="left" )
print(sales_with_product)

#Show which Product_Name is stored in which Location.
product_location = pd.merge(inventory,warehouses,on="Warehouse_ID",how="left")
print(product_location)

#Create a report of all products in the inventory and the Manager responsible for them.
product_manager_report = pd.merge(
    inventory,
    warehouses,
    on="Warehouse_ID",
    how="left"
)
print(product_manager_report)

#Display a list of all Transaction_IDs and the Product_Name associated with them, but only for items currently in our inventory.
transaction_report = pd.merge(
    sales,
    inventory,
    on="SKU",
    how="left"
)
print(transaction_report)

#Identify which products in our inventory have zero sales recorded.
merged1 = pd.merge(
    inventory,
    warehouses,
    on="Warehouse_ID",
    how="left"
)
print(merged1)

#Find the SKU of the item that was sold in sales but does not exist in our inventory records.
merged2=pd.merge(
    inventory,
    sales,
    on="SKU",
    how="left"
)
print(merged2)

missing_warehouse = pd.merge(
    inventory,
    warehouses,
    on="Warehouse_ID",
    how="left",
)
print(missing_warehouse)

#List all warehouse Locations that currently do not have any products from our inventory stored in them.
unused_locations = pd.merge(
    warehouses,
    inventory,
    on="Warehouse_ID",
    how="left",
)
print(unused_locations)

#Create a master list of all unique SKUs mentioned across both the inventory and sales tables, regardless of whether they match.
master_sku_list = pd.merge(
    inventory,
    sales,
    on="SKU",
    how="outer"
)
print(master_sku_list)

# Which Manager oversaw the sale of the "Webcam"?
webcam_manager = pd.merge(
    sales,
    inventory,
    on="SKU",
    how="inner"
)
webcam_manager = pd.merge(
    inventory,
    warehouses,
    on="Warehouse_ID",
    how="left"
)
print(webcam_manager)

#Generate a report of all sales, including the Location of the warehouse the product came from.
sales_report = pd.merge(
    sales,
    inventory,
    on="SKU",
    how="left"
)
sales_report = pd.merge(
    sales_report,
    warehouses,
    on="Warehouse_ID",
    how="left"
)
print(sales_report)

#Show only the products that are out of stock (Stock_Level is 0) and check if any sales were made for them.
out_of_stock = pd.merge(
    inventory,
    sales,
    on="SKU",
    how="right"
)
print(out_of_stock)

#Find the total Quantity_Sold for each Location.
location_sales = pd.merge(
    sales,
    inventory,
    on="SKU",
    how="left"
)
location_sales = pd.merge(
    location_sales,
    warehouses,
    on="Warehouse_ID",
    how="left"
)
print(location_sales)

#List all transactions that occurred on '2024-01-02' and include the Product_Name and Stock_Level for those items.
transactions_0202 = pd.merge(
    sales[sales["Sale_Date"] == "2024-01-02"],
    inventory,
    on="SKU",
    how="left"
)
print(transactions_0202)

#Calculate the "Remaining Stock" for each product by subtracting Quantity_Sold from Stock_Level. (Hint: Treat missing sales as 0).
remaining_stock = pd.merge(
    inventory,
    sales.groupby("SKU")["Quantity_Sold"].sum().reset_index(),
    on="SKU",
    how="left"
)
remaining_stock["Quantity_Sold"] = remaining_stock["Quantity_Sold"].fillna(0)
remaining_stock["Remaining_Stock"] = (
    remaining_stock["Stock_Level"] - remaining_stock["Quantity_Sold"]
)
print(remaining_stock[["Product_Name", "Remaining_Stock"]])
# Identify any Transaction_ID where we sold an item, but we have no record of which Warehouse_ID it came from.
missing_warehouse_txn = pd.merge(
    sales,
    inventory[["SKU", "Warehouse_ID"]],
    on="SKU",
    how="left"
)
print(missing_warehouse_txn)
# Produce a table that shows every Product_Name and every Location, ensuring that products without locations and locations without products are both visible.
full_view = pd.merge(
    inventory[["Product_Name", "Warehouse_ID"]],
    warehouses[["Warehouse_ID", "Location"]],
    on="Warehouse_ID",
    how="outer"
)
print(full_view)
# Find the Manager who has the highest total Stock_Level under their supervision.
manager_stock = pd.merge(
    inventory,
    warehouses[["Warehouse_ID", "Manager"]],
    on="Warehouse_ID",
    how="left"
)
highest_manager = (
    manager_stock
    .groupby("Manager")["Stock_Level"]
    .sum()
    .sort_values(ascending=False)
)
print(highest_manager)
# Create a final "Executive Report" containing Transaction_ID, Product_Name, Quantity_Sold, Location, and Manager. Ensure no sales data is deleted, even if product details are missing.
executive_report = pd.merge(
    sales,
    inventory[["SKU", "Product_Name", "Warehouse_ID"]],
    on="SKU",
    how="left"
)
executive_report = pd.merge(
    executive_report,
    warehouses[["Warehouse_ID", "Location", "Manager"]],
    on="Warehouse_ID",
    how="left"
)
print(executive_report)