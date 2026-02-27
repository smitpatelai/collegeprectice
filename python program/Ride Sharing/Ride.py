import pandas as pd

trips = pd.read_csv("trips.csv")
drivers = pd.read_csv("driver.csv")
riders = pd.read_csv("riders.csv")
payments = pd.read_csv("payments.csv")

trips.columns = trips.columns.str.strip()
drivers.columns = drivers.columns.str.strip()
riders.columns = riders.columns.str.strip()
payments.columns = payments.columns.str.strip()

print("\nTrips Columns:", trips.columns)
print("Drivers Columns:", drivers.columns)
print("Riders Columns:", riders.columns)
print("Payments Columns:", payments.columns)

df1 = trips.merge(drivers, on="Driver_ID", how="left")
df2 = df1.merge(riders, on="Rider_ID", how="left")
master_df = df2.merge(payments, on="Trip_ID", how="left")

print("\nMaster Dataset Shape:", master_df.shape)

inactive_drivers = drivers[~drivers["Driver_ID"].isin(trips["Driver_ID"])]
print("\nInactive Drivers:")
print(inactive_drivers)

inactive_riders = riders[~riders["Rider_ID"].isin(trips["Rider_ID"])]
print("\nInactive Riders:")
print(inactive_riders)

if "Payment_Status" in master_df.columns:
    master_df["Payment_Status"] = master_df["Payment_Status"].fillna("Cancelled")

amount_columns = [col for col in master_df.columns if "amount" in col.lower()]

if amount_columns:
    master_df[amount_columns[0]] = master_df[amount_columns[0]].fillna(0)
    print("\nFilled missing values in:", amount_columns[0])
else:
    print("\nNo Amount column found")

print("\nMissing Values in Master Dataset:")
print(master_df.isnull().sum())

if "Trip_ID" in master_df.columns:
    print("\nDuplicate Trip_ID Count:", master_df["Trip_ID"].duplicated().sum())

print("\nTrips Rows:", trips.shape[0])
print("Master Rows:", master_df.shape[0])

if trips.shape[0] == master_df.shape[0]:
    print("\nData Merge Successful !!")
else:
    print("\nRow count mismatch ? Check joins")

print("\nFinal Master Dataset Preview:")
print(master_df.head())