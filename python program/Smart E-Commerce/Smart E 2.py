import pandas as pd

df = pd.read_csv("ecomdataset.csv")


print("\n===== FIRST 10 ROWS =====")
print(df.head(10))

print("\n===== DATASET SHAPE =====")
print(df.shape)

print("\n===== DATA TYPES =====")
print(df.dtypes)

print("\n===== STATISTICAL SUMMARY =====")
print(df.describe())

print("\n===== MISSING VALUES COUNT =====")
print(df.isnull().sum())

print("\n===== MISSING VALUES PERCENTAGE =====")
print((df.isnull().sum() / len(df)) * 100)

print("\n===== TEXT COLUMNS =====")
print(df.select_dtypes(include=["object", "string"]).columns)

numeric_cols = ["Price", "Quantity", "Discount_Percent",
                "Rating", "Delivery_Days"]

for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

mean_price = df["Price"].mean()
df["Price"] = df["Price"].fillna(mean_price)
df.loc[df["Price"] <= 0, "Price"] = mean_price

df["Quantity"] = df["Quantity"].fillna(1)
df.loc[df["Quantity"] <= 0, "Quantity"] = 1

median_discount = df["Discount_Percent"].median()
df["Discount_Percent"] = df["Discount_Percent"].fillna(median_discount)

df.loc[df["Discount_Percent"] < 0, "Discount_Percent"] = 0
df.loc[df["Discount_Percent"] > 100, "Discount_Percent"] = median_discount

median_rating = df["Rating"].median()
df["Rating"] = df["Rating"].fillna(median_rating)

df.loc[df["Rating"] < 0, "Rating"] = 0
df.loc[df["Rating"] > 5, "Rating"] = 5

median_delivery = df["Delivery_Days"].median()
df["Delivery_Days"] = df["Delivery_Days"].fillna(median_delivery)

text_lower_cols = ["Order_Status", "Return_Status", "Payment_Method"]

for col in text_lower_cols:
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip().str.lower()

if "Category" in df.columns:
    df["Category"] = df["Category"].astype(str).str.strip().str.title()

print("\nText Standardization Completed ✅")

print("\n===== FINAL MISSING VALUES =====")
print(df.isnull().sum())
print("===============================================================================================================")
print("\n===== DATA LOADED SUCCESSFULLY =====")
print("Dataset Shape:", df.shape)

# Convert numeric columns safely
numeric_cols = ["Price", "Quantity", "Discount_Percent",
                "Rating", "Delivery_Days"]

for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# Fill Missing Values
df["Price"] = df["Price"].fillna(df["Price"].mean())
df["Quantity"] = df["Quantity"].fillna(1)
df["Discount_Percent"] = df["Discount_Percent"].fillna(0)
df["Rating"] = df["Rating"].fillna(df["Rating"].median())
df["Delivery_Days"] = df["Delivery_Days"].fillna(df["Delivery_Days"].median())

# Fix invalid values
df.loc[df["Price"] <= 0, "Price"] = df["Price"].mean()
df.loc[df["Quantity"] <= 0, "Quantity"] = 1
df.loc[df["Discount_Percent"] < 0, "Discount_Percent"] = 0
df.loc[df["Discount_Percent"] > 100, "Discount_Percent"] = 100
df.loc[df["Rating"] < 0, "Rating"] = 0
df.loc[df["Rating"] > 5, "Rating"] = 5

# Standardize text columns
text_cols_lower = ["Order_Status", "Return_Status", "Payment_Method"]

for col in text_cols_lower:
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip().str.lower()

if "Category" in df.columns:
    df["Category"] = df["Category"].astype(str).str.strip().str.title()

print("\nData Cleaning Completed ✅")

# Financial Calculations
df["Discounted_Price"] = df["Price"] * (1 - df["Discount_Percent"] / 100)
df["Total_Order_Value"] = df["Discounted_Price"] * df["Quantity"]
df["Platform_Commission"] = df["Total_Order_Value"] * 0.15
df["Seller_Earnings"] = df["Total_Order_Value"] * 0.85

# IMPORTANT: Create float columns to avoid dtype error
df["Shipping_Cost"] = 0.0
df["Return_Cost"] = 0.0

# Shipping Rules
df.loc[df["Total_Order_Value"] < 500, "Shipping_Cost"] = 60.0
df.loc[(df["Total_Order_Value"] >= 500) &
       (df["Total_Order_Value"] <= 1500), "Shipping_Cost"] = 40.0
df.loc[df["Total_Order_Value"] > 1500, "Shipping_Cost"] = 0.0

# Return Cost (10% if returned)
df.loc[df["Return_Status"] == "yes",
       "Return_Cost"] = df["Total_Order_Value"] * 0.10

# Estimated Profit
df["Estimated_Profit"] = (
    df["Platform_Commission"]
    - df["Shipping_Cost"]
    - df["Return_Cost"]
)

print("\nBusiness Calculations Completed ✅")

# Business Summary
print("\n===== BUSINESS SUMMARY =====")
print("Total Revenue:", df["Platform_Commission"].sum())
print("Total Shipping Cost:", df["Shipping_Cost"].sum())
print("Total Return Cost:", df["Return_Cost"].sum())
print("Total Estimated Profit:", df["Estimated_Profit"].sum())
print("Average Profit Per Order:", df["Estimated_Profit"].mean())

# Total Spend Per Customer
customer_spend = df.groupby("Customer_ID")["Total_Order_Value"].sum().reset_index()

customer_spend = customer_spend.sort_values(
    by="Total_Order_Value", ascending=False)

print("\n===== TOTAL SPEND PER CUSTOMER =====")
print(customer_spend)

# Top 5 Customers
top5 = customer_spend.head(5)

total_revenue = df["Total_Order_Value"].sum()
top5_percent = (top5["Total_Order_Value"].sum() / total_revenue) * 100

print("\n===== TOP 5 CUSTOMERS =====")
print(top5)
print("Top 5 Revenue Contribution (%):", top5_percent)

# Frequent Customers (>5 orders)
order_count = df.groupby("Customer_ID").size().reset_index(name="Order_Count")

frequent_customers = order_count[order_count["Order_Count"] > 5]

print("\n===== FREQUENT CUSTOMERS (>5 Orders) =====")
print(frequent_customers)

# High Return Rate (>40%)
total_orders = df.groupby("Customer_ID").size().reset_index(name="Total_Orders")
returned_orders = df[df["Return_Status"] == "yes"] \
    .groupby("Customer_ID").size().reset_index(name="Returned")

return_analysis = total_orders.merge(returned_orders,
                                     on="Customer_ID",
                                     how="left")

return_analysis["Returned"] = return_analysis["Returned"].fillna(0)

return_analysis["Return_%"] = (
    return_analysis["Returned"] /
    return_analysis["Total_Orders"]
) * 100

high_return = return_analysis[return_analysis["Return_%"] > 40]

print("\n===== HIGH RETURN CUSTOMERS (>40%) =====")
print(high_return)

# Low Satisfaction Customers (Rating < 3)
customer_rating = df.groupby("Customer_ID")["Rating"].mean().reset_index()

low_satisfaction = customer_rating[customer_rating["Rating"] < 3]

print("\n===== LOW SATISFACTION CUSTOMERS =====")
print(low_satisfaction)

def segment(spend):
    if spend > 10000:
        return "Platinum"
    elif spend >= 5000:
        return "Gold"
    elif spend >= 2000:
        return "Silver"
    else:
        return "Bronze"

customer_spend["Customer_Segment"] = \
    customer_spend["Total_Order_Value"].apply(segment)

df = df.merge(customer_spend[["Customer_ID",
                              "Customer_Segment"]],
              on="Customer_ID",
              how="left")

print("\nSegmentation Completed ✅")

# Segment Distribution
segment_counts = customer_spend["Customer_Segment"].value_counts()
print("\n===== CUSTOMER SEGMENT DISTRIBUTION =====")
print(segment_counts)

# Revenue by Segment
segment_revenue = df.groupby("Customer_Segment")[
    "Total_Order_Value"].sum()

print("\n===== REVENUE BY SEGMENT =====")
print(segment_revenue)

total_customers = df["Customer_ID"].nunique()
avg_orders = len(df) / total_customers
avg_spend = customer_spend["Total_Order_Value"].mean()

print("\n===== CUSTOMER INSIGHTS SUMMARY =====")
print("Total Unique Customers:", total_customers)
print("Average Orders Per Customer:", avg_orders)
print("Average Spend Per Customer:", avg_spend)
print("High Return Customers:", len(high_return))
print("Low Satisfaction Customers:", len(low_satisfaction))

print("\nPROJECT COMPLETED SUCCESSFULLY ✅")