import pandas as pd

# LOAD DATA FROM FILE
df = pd.read_csv("ecomorders.csv")
print(df)

print(df["Category"])

# multiple col
print(df[["Category","Price"]])

# find null values
print(df.isnull().sum())

# convert price to numeric ( invalid data handle )
df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
print(df["Price"])

# convert quantity to numeric
df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
print(df["Quantity"])

# convert rating to numeric
df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")
print(df["Rating"])

print("\n After Converting Data in Numerics: ")
print(df[["Price","Quantity","Rating"]])

# -- HANDLE MISSING VALUES
# FILL MISSING VALUE

mean_price = df["Price"].mean()
print(mean_price)

# fill Nan with mean price
df.fillna(value={"Price": mean_price}, inplace=True)

print(df["Price"])

# fill quantity values
df.fillna(value={"Quantity": 1}, inplace=True)

# fill rating values
mean_rating = df["Rating"].mean()
df.fillna(value={"Rating": mean_rating}, inplace=True)

print("\n Data After Missing Values: ")
print(df[["Price","Quantity","Rating"]])

# filter and update data
df.loc[df["Price"] < 0, "Price"] = mean_price

print(df["Price"])

df.loc[df["Quantity"] <= 0, "Quantity"] = 1

df.loc[df["Rating"] < 0, "Rating"] = 0
df.loc[df["Rating"] > 5, "Rating"] = 5

print(df[["Quantity","Rating"]])

df["Total"] = round(df["Price"] * df["Quantity"], 2)

print(df)

df["Quantity"] = df["Quantity"].astype(int)

print(df.info())

highest_order = df["Total"].max()
print(highest_order)

df.to_csv("final_cleaned_data.csv", index=False)
print("Data Stored")
