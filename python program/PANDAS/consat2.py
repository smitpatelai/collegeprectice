import pandas as pd
from fontTools.ttLib.tables.otTraverse import dfs_base_table

#Step 1 — Create the DataFrame
data = {
    "Seat1": [
    "Available", "Booked", "Available", "Available", "Booked", "Available", "Available", "Booked", "Available"
 ],
    "Seat2": [
    "Booked", "Available", "Available", "Booked", "Available", "Booked", "Available", "Available", "Booked"
 ],
    "Seat3": [
    "Available", "Booked", "Booked", "Available", "Booked", "Available", "Booked", "Available", "Available"
 ],
   " Seat4": [
    "Booked", "Available", "Booked", "Available", "Available", "Booked", "Available", "Booked", "Available"
 ],
    "Seat5": [
    "Available", "Available", "Available", "Booked", "Available", "Available", "Booked", "Available", "Booked"
 ]
 }

df=pd.DataFrame(data,index=["VIP", "VIP", "VIP",
        "Premium", "Premium", "Premium",
        "Classic", "Classic", "Classic"])

#Step 2 — Display the DataFrame
print("Concert Seating Layout:")
print(df)


# Count available seats per row
df["Available_Count"] = (df == "Available").sum(axis=1)
print(df)

# Count booked seats per row
df["Booked_Count"] = (df == "Booked").sum(axis=1)
print(df)
# Availability ratio per row
df["Availability_Ratio"] = df["Available_Count"] / (
    df["Available_Count"] + df["Booked_Count"]
)
print(df)

# Calculate total available seats per section.
print(df.groupby(df.index)["Available_Count"].sum())

#Calculate total booked seats per section.
print(df.groupby(df.index)["Booked_Count"].sum())

#Find average availability ratio per section.
print(df.groupby(df.index)["Availability_Ratio"].mean())

#Find maximum Available_Count in each section.
print(df.groupby(df.index)["Available_Count"].max())

#Find minimum Available_Count in each section.
print(df.groupby(df.index)["Available_Count"].min())

#Count total rows per section.
df.groupby(df.index).size()
print(df)

#— TRANSFORM TASKS
#Add a column Section_Total_Available using transform.
df["Section_Total_Available"] = df.groupby(df.index) ["Available_Count"].transform("sum")
print(df)

#Add a column Section_Total_Booked using transform.
df["Section_Total_Booked"]=df.groupby(df.index)["Booked_Count"].transform("sum")
print(df)

#Add a column showing each row’s contribution percentage to its section’s total availability.
df["Availability_Contribution_%"] = (
    df["Available_Count"]
    / df["Section_Total_Available"]
) * 100
df["Availability_Contribution_%"] = df["Availability_Contribution_%"].round(2)
print(df)

# — APPLY TASKS
# Create a column Row_Status:
def row_status(x):
    if x == 0:
        return "Full"
    elif x == 5:
        return "Empty"
    else:
        return "Partial"

df["Row_Status"] = df["Available_Count"].apply(row_status)
print(df)
#Create a column Booking_Priority:
def booking_priority(x):
    if x <= 1:
        return "High"
    elif 2 <= x <= 3:
        return "Medium"
    else:
        return "Low"

df["Booking_Priority"] = df["Available_Count"].apply(booking_priority)
print(df)
# Create a column Risk_Level:
def risk_level(x):
    if x < 0.20:
        return "Critical"
    elif 0.20 <= x <= 0.50:
        return "Moderate"
    else:
        return "Safe"

df["Risk_Level"] = df["Availability_Ratio"].apply(risk_level)
print(df)
# Create a column Revenue_Class assuming section price mapping:
price_map = {
    "VIP": 5000,
    "Premium": 3000,
    "Classic": 1500
}

df["Revenue_Class"] = df.index.map(price_map)
print(df)


# — RANKING TASKS
# Rank rows inside each section based on Available_Count (descending).
df["Rank_Available_Section"] = (
    df.groupby(df.index)["Available_Count"]
      .rank(method="dense", ascending=False)
)
print(df)
# Rank rows inside each section based on Booked_Count (descending).
df["Rank_Booked_Section"] = (
    df.groupby(df.index)["Booked_Count"]
      .rank(method="dense", ascending=False)
)
print(df)
# Rank rows overall based on Available_Count.
df["Rank_Available_Overall"] = (
    df["Available_Count"]
      .rank(method="dense", ascending=False)
)
print(df)
#
# — WINDOW LOGIC TASKS
# Show top 2 rows per section with highest Available_Count.
top2_available = (
    df.sort_values(["Available_Count"], ascending=False)
      .groupby(df.index)
      .head(2)
)
print(top2_available)
# Show bottom 2 rows per section with lowest Available_Count.
bottom2_available = (
    df.sort_values(["Available_Count"], ascending=True)
      .groupby(df.index)
      .head(2)
)
print(bottom2_available)
# Show top 1 row per section with highest Booked_Count.
top1_booked = (
    df.sort_values(["Booked_Count"], ascending=False)
      .groupby(df.index)
      .head(1)
)
print(top1_booked)