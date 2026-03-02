import pandas as pd
# Load dataset
df = pd.read_csv("ecomdataset.csv")   # Change filename if needed

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

print("\nDataset Cleaned Successfully ✅")

# 2.1 Discounted Price
df["Discounted_Price"] = df["Price"] * (
    1 - df["Discount_Percent"] / 100
)

# 2.2 Total Order Value
df["Total_Order_Value"] = (
    df["Discounted_Price"] * df["Quantity"]
)

# 2.3 Platform Commission (15%)
df["Platform_Commission"] = (
    df["Total_Order_Value"] * 0.15
)

# 2.4 Seller Earnings (85%)
df["Seller_Earnings"] = (
    df["Total_Order_Value"] * 0.85
)
# 2.5 Shipping Cost (float column to avoid dtype errors)
df["Shipping_Cost"] = 0.0

df.loc[df["Total_Order_Value"] < 500,
       "Shipping_Cost"] = 60.0

df.loc[(df["Total_Order_Value"] >= 500) &
       (df["Total_Order_Value"] <= 1500),
       "Shipping_Cost"] = 40.0

df.loc[df["Total_Order_Value"] > 1500,
       "Shipping_Cost"] = 0.0

# 2.6 Return Cost (10% if returned)
df["Return_Cost"] = 0.0

df.loc[df["Return_Status"] == "yes",
       "Return_Cost"] = (
           df.loc[df["Return_Status"] == "yes",
                  "Total_Order_Value"] * 0.10
       )
# 2.7 Estimated Profit
df["Estimated_Profit"] = (
    df["Platform_Commission"]
    - df["Shipping_Cost"]
    - df["Return_Cost"]
)
print("\n===== BUSINESS SUMMARY =====")

print("Total Platform Revenue:",
      df["Platform_Commission"].sum())

print("Total Shipping Cost:",
      df["Shipping_Cost"].sum())

print("Total Return Cost:",
      df["Return_Cost"].sum())

print("Total Estimated Profit:",
      df["Estimated_Profit"].sum())

print("Average Profit Per Order:",
      df["Estimated_Profit"].mean())

print("\nFinal Dataset Preview:")
print(df.head())

customer_spend = (
    df.groupby("Customer_ID")["Total_Order_Value"]
    .sum()
    .reset_index()
)

customer_spend = customer_spend.sort_values(
    by="Total_Order_Value",
    ascending=False
)

print("\n===== TOTAL SPEND PER CUSTOMER =====")
print(customer_spend)

top5_customers = customer_spend.head(5)

print("\n===== TOP 5 CUSTOMERS =====")
print(top5_customers)

total_revenue = df["Total_Order_Value"].sum()
top5_revenue = top5_customers["Total_Order_Value"].sum()

top5_percentage = (top5_revenue / total_revenue) * 100

print("\nTop 5 Customers Contribution (%):", top5_percentage)

customer_orders = (
    df.groupby("Customer_ID")
    .size()
    .reset_index(name="Order_Count")
)

frequent_customers = customer_orders[
    customer_orders["Order_Count"] > 5
]

print("\n===== FREQUENT CUSTOMERS (>5 Orders) =====")
print(frequent_customers)

frequent_percentage = (
    len(frequent_customers) / len(customer_orders)
) * 100

print("\nFrequent Customers Percentage:", frequent_percentage)

# Count total orders
total_orders = (
    df.groupby("Customer_ID")
    .size()
    .reset_index(name="Total_Orders")
)

# Count returned orders
returned_orders = (
    df[df["Return_Status"] == "yes"]
    .groupby("Customer_ID")
    .size()
    .reset_index(name="Returned_Orders")
)

# Merge both
return_analysis = total_orders.merge(
    returned_orders,
    on="Customer_ID",
    how="left"
)

return_analysis["Returned_Orders"] = (
    return_analysis["Returned_Orders"].fillna(0)
)

# Calculate return rate
return_analysis["Return_Rate_%"] = (
    return_analysis["Returned_Orders"]
    / return_analysis["Total_Orders"]
) * 100

high_return_customers = return_analysis[
    return_analysis["Return_Rate_%"] > 40
]

print("\n===== HIGH RETURN RATE CUSTOMERS (>40%) =====")
print(high_return_customers)

customer_rating = (
    df.groupby("Customer_ID")["Rating"]
    .mean()
    .reset_index()
)

low_satisfaction = customer_rating[
    customer_rating["Rating"] < 3.0
]

print("\n===== LOW SATISFACTION CUSTOMERS =====")
print(low_satisfaction)

print("\nTotal Low Satisfaction Customers:",
      len(low_satisfaction))

# Create segment column
def segment_customer(spend):
    if spend > 10000:
        return "Platinum"
    elif 5000 <= spend <= 10000:
        return "Gold"
    elif 2000 <= spend < 5000:
        return "Silver"
    else:
        return "Bronze"

customer_spend["Customer_Segment"] = (
    customer_spend["Total_Order_Value"]
    .apply(segment_customer)
)

# Merge segmentation back to main dataset
df = df.merge(
    customer_spend[["Customer_ID", "Customer_Segment"]],
    on="Customer_ID",
    how="left"
)

print("\nSegmentation Applied Successfully ✅")

segment_counts = (
    customer_spend["Customer_Segment"]
    .value_counts()
    .reset_index()
)
segment_counts.columns = ["Segment", "Customer_Count"]

segment_counts["Percentage_%"] = (
    segment_counts["Customer_Count"]
    / len(customer_spend)
) * 100
print("\n===== CUSTOMER SEGMENT DISTRIBUTION =====")
print(segment_counts)
# Revenue by segment
segment_revenue = (
    df.groupby("Customer_Segment")["Total_Order_Value"]
    .sum()
    .reset_index()
)
print("\n===== REVENUE BY SEGMENT =====")
print(segment_revenue)
# Average Order Value per segment
segment_aov = (
    df.groupby("Customer_Segment")["Total_Order_Value"]
    .mean()
    .reset_index()
)
print("\n===== AVERAGE ORDER VALUE BY SEGMENT =====")
print(segment_aov)

total_customers = df["Customer_ID"].nunique()
total_orders_count = len(df)

avg_orders_per_customer = (
    total_orders_count / total_customers
)

avg_spend_per_customer = (
    customer_spend["Total_Order_Value"].mean()
)
print("\n===== CUSTOMER INSIGHTS SUMMARY =====")
print("Total Unique Customers:", total_customers)
print("Average Orders Per Customer:", avg_orders_per_customer)
print("Average Spend Per Customer:", avg_spend_per_customer)
print("Top 5 Revenue Contribution (%):", top5_percentage)
print("Frequent Buyers (%):", frequent_percentage)
print("High Return Customers:", len(high_return_customers))
print("Low Satisfaction Customers:", len(low_satisfaction))