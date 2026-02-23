import pandas as pd

data = {
    "Users":["Amit","Raj","Neha","Amit","Raj","Neha","Amit"],
    "city":["Mumbai","Delhi","Mumbai","Delhi","Mumbai","Delhi","Mumbai"],
    "product":["Coffee","Bread","Coffee","Bread""Coffee","Bread","Coffee"],
    "category":["Dairy","Bakery","Dairy","Bakery","Dairy","Bakery","Dairy"],
    "quantity":[11,42,63,14,52,60,30],
    "price":[600,450,430,220,180,320,500]
}

df = pd.DataFrame(data)
print(df)

df["total"] = df["quantity"] * df["price"]
print(df)

print(df.head(2))
print(type(df))


print("Total Sales per City")

