import pandas as pd
from contextlib import nullcontext

df = pd.read_csv("food_delivery_orders.csv")
# <----------------------------m TASK 1 --------------------->
print(df)
print(df.head(10))
print(df.shape)
print(df.describe())
print(df.info())

# <----------------------------m TASK 1 --------------------->
missing_counts = df.isnull().sum()
columns_with_nulls = missing_counts[missing_counts > 0]
print("--- Missing Values Count ---")
print(columns_with_nulls)

missing_percentage = (df.isnull().sum() / len(df))*100
print("\n--- Percentage of Missing Data in % : ---")
print(missing_percentage[missing_percentage > 0].round(2))
print("Date Type use :")
print(df.dtypes)

# <---------------------------  For Price ---------------------------------->
df["Price"] = pd.to_numeric(df["Price"],errors="coerce")
mean_price = df["Price"].mean()
df.fillna({"Price":mean_price},inplace=True)
df.loc[df["Price"]<0,"Price"] = mean_price
df["Price"] = round(df["Price"],2).astype(int)
print(df["Price"])
print("\n\n\n Count OF NUll Values In Price =",df["Price"].isnull().sum())

# <--------------------------- For Quantity ----------------------------------->
df["Quantity"] = pd.to_numeric(df["Quantity"],errors="coerce")
df.fillna({"Quantity":1},inplace=True)
print(df.fillna)
df.loc[df["Quantity"]<0,"Quantity"] = 1
df["Quantity"] = df["Quantity"].astype(int)
print(df["Quantity"])

# <--------------------------- For Delivery Time  ----------------------------------->
df["Delivery_Time_Minutes"] = pd.to_numeric(df["Delivery_Time_Minutes"],errors="coerce")
median_dlvtime = df["Delivery_Time_Minutes"].median()
df.fillna({"Delivery_Time_Minutes":median_dlvtime},inplace=True)
df["Delivery_Time_Minutes"] = round(df["Delivery_Time_Minutes"],2).astype(int)
print(df["Delivery_Time_Minutes"])


# <--------------------------- For Rating----------------------------------->
df["Rating"] = pd.to_numeric(df["Rating"],errors="coerce")
mean_rating = df["Rating"].mean()

df.fillna({"Rating":mean_rating},inplace=True)
df.loc[df["Rating"]>5,"Rating"] = 5
df["Rating"] = round(df["Rating"],2)
print(df["Rating"])

df["Total"] = df["Price"] * df["Quantity"]

df["Order_Status"] = df["Order_Status"].str.lower()
df["Payment_Method"] = df["Payment_Method"].str.lower()

text_cols = df.select_dtypes(include=['string']).columns
for col in text_cols:
    df[col] = df[col].str.strip()

print("--- Standardized Order Status ---")
print(df['Order_Status'].unique())

print("\n--- Standardized Payment Method ---")
print(df['Payment_Method'].unique())


print("<--------------------- Finale Stage ----------------------------->")
print("Missing Values Count :")
print(df.isnull().sum())

numeric_cols = df.select_dtypes(include=['number']).columns

print("--- Numerical Validity Check ---")
for col in numeric_cols:
    inf_count = (df[col] == float('inf')).sum()
    print(f"{col}: {df[col].dtype} | Infs: {inf_count}")
print("\nSuggested review (Object columns):")
print(df.select_dtypes(include=['number']).columns.tolist())

print("\n--- CLEAN DATASET SUMMARY ---")
print(df.info())
print("\n--- Final Statistical Snapshot ---")
print(df.describe())

print("<-------------------------Calculate Platform Commission------------------------>")
print("<------------------------------ 2nd Implimentation ---------------------------------->")
df["Total_Bill"] = df["Price"] * df["Quantity"]
print(df["Total_Bill"])
df["Platfrom_Commision"] = df["Total_Bill"] *0.2
df["Platfrom_Commision"] = df["Platfrom_Commision"].round().astype(int)
print(df["Platfrom_Commision"])


df["Restaurant_Earning"] = df["Total_Bill"] - df["Platfrom_Commision"].round().astype(int)
print(df["Restaurant_Earning"])

print((df["Total_Bill"] * 0.8).round().astype(int))

print("<-------------------------Implement Distance-Based Delivery Cost------------------------>")

df["Delivery_Distance_KM"] = pd.to_numeric(df["Delivery_Distance_KM"], errors="coerce")

df.loc[df["Delivery_Distance_KM"] < 5, "Delivery_Cost"] = 20
df.loc[(df["Delivery_Distance_KM"] >= 5) & (df["Delivery_Distance_KM"] <= 10), "Delivery_Cost"] = 40
df.loc[df["Delivery_Distance_KM"] > 10, "Delivery_Cost"] = 60

df["Delivery_Cost"] = df["Delivery_Cost"].astype(int)

print(df[["Delivery_Distance_KM", "Delivery_Cost"]])

print("\nDelivery Cost Verification:")
print(df.groupby("Delivery_Cost")["Delivery_Distance_KM"].count())


print("<-------------------------Calculate Estimated Profit------------------------>")

df["Estimated_Profit"] = df["Platfrom_Commision"] - df["Delivery_Cost"]

print(df[["Platfrom_Commision", "Delivery_Cost", "Estimated_Profit"]])

print("\nProfit Verification:")
print((df["Platfrom_Commision"] - df["Delivery_Cost"]).equals(df["Estimated_Profit"]))


print("<-------------------------Business Model Validation------------------------>")

total_revenue = df["Platfrom_Commision"].sum()
total_delivery_cost = df["Delivery_Cost"].sum()
total_profit = df["Estimated_Profit"].sum()
avg_profit_per_order = df["Estimated_Profit"].mean()    

print("Total Revenue (Platform Commission) :", total_revenue)
print("Total Delivery Cost :", total_delivery_cost)
print("Total Estimated Profit :", total_profit)
print("Average Profit Per Order :", round(avg_profit_per_order,2)).astype(int)


df.to_csv("cleaned_food_delivery_orders.csv",index=False)
print("Data Stored")