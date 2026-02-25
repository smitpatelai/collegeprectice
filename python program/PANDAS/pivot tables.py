import pandas as pd

data = {
"Salesperson": ["Amit", "Amit", "Amit", "Neha", "Neha", "Neha",
"Raj", "Raj", "Raj", "Priya", "Priya", "Priya"],

"Region": ["North", "South", "West", "North", "South", "West",
"North", "South", "West", "North", "South", "West"],

"Product": ["Laptop", "Laptop", "Laptop", "Laptop", "Laptop", "Laptop",
"Mobile", "Mobile", "Mobile", "Mobile", "Mobile", "Mobile"],

"Quarter": ["Q1", "Q2", "Q3", "Q1", "Q2", "Q3",
"Q1", "Q2", "Q3", "Q1", "Q2", "Q3"],

"Units_Sold": [10, 8, 12, 9, 11, 7, 20, 18, 25, 15, 14, 19],

"Revenue": [5888, 488888, 688888, 458888, 558880, 358888,
300000, 280000, 400000, 250000, 240000, 350000]
}

df = pd.DataFrame(data)
print(df)


print(df.groupby("Region")["Revenue"].sum())

print("\n Revenue per Region")

pivot1 = pd.pivot_table(
df,
values="Revenue",
index="Region",
aggfunc="sum"
)

print(pivot1)

print("\n Revenue by product and region")

pivot2 = pd.pivot_table(
df,
values="Revenue",
index="Region",
columns="Product",
aggfunc="sum"
)

print(pivot2)

print("\n Unit sold per quarter")

pivot3 = pd.pivot_table(
df,
values="Units_Sold",
index="Quarter",
aggfunc="sum"
)

print(pivot3)

pivot4 = pd.pivot_table(
df,
values="Revenue",
index="Region",
aggfunc=["sum","mean"]
)

print(pivot4)

pivot5 = pd.pivot_table(
df,
values="Revenue",
index="Region",
columns="Product",
aggfunc="sum",
margins=True
)

print(pivot5["Laptop"]["North"])

pivot6 = pd.pivot_table(
df,
values="Revenue",
index=["Salesperson","Region"],
columns="Quarter",
aggfunc="sum",
margins=True,
fill_value=0
)

print(pivot6)
print(pivot6.loc[("Neha","North"),"Q1"])

# delhi - 12 , 1500
# mumbai - 6 - 1208
