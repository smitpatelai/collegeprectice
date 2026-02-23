import pandas as pd

data = {
    "Users":["Amit","Raj","Neha","Amit","Raj","Neha","Amit"],
    "city":["Mumbai","Delhi","Mumbai","Delhi","Mumbai","Delhi","Mumbai"],
    "product":["Coffee","Bread","Coffee","Bread","Coffee","Bread","Coffee"],
    "category":["Dairy","Bakery","Dairy","Bakery","Dairy","Bakery","Dairy"],
    "quantity":[11,42,63,14,52,60,30],
    "price":[600,450,430,220,180,320,500]
}

df = pd.DataFrame(data)
print(df)

# Create total column
df["total"] = df["quantity"] * df["price"]
print(df)

print(df.head(2))
print(type(df))


print("Total Sales per City")
print(df.groupby("city")["total"].sum())


# min , max , avg , sum , count
print("City Summary: Sales , Quantity")
print(df.groupby("city").agg(
    {
        "total":"sum",
        "quantity":"mean"
    }
))


# add column city_total in df
df["city_total"] = df.groupby("city")["total"].transform("sum")
print(df)


# APPLY
def order_size(x):
    if x > 1000:
        return "BIG"
    else:
        return "SMALL"

df["order_type"] = df["total"].apply(order_size)
print(df)


# FILTER
print(df[df["order_type"] == "BIG"].max())
print(df[df["order_type"] == "BIG"].head(1))


# RANK
df["city_rank"] = df.groupby("city")["total"].rank(ascending=False)
print(df.sort_values("city_rank").head(4))


# WINDOW (Top 2 per city)
top2 = df.sort_values(by="total", ascending=False).groupby("city").head(2)
print(top2)


# CROSSTAB
print(pd.crosstab(df["city"], df["product"]))