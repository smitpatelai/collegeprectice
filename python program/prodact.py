import requests

url = "https://fakestoreapi.com/products"

products = requests.get(url).json()

print("Total Products:", len(products))

prices = []
categories = {}
high_demand = []

for p in products:
    prices.append(p["price"])

    # Category-wise price storage
    cat = p["category"]
    categories.setdefault(cat, []).append(p["price"])

    # Demand pattern (rating count > 200)
    if p["rating"]["count"] > 200:
        high_demand.append(p["title"])

print("\nPrice Analysis")
print("Maximum Price:", max(prices))
print("Minimum Price:", min(prices))
print("Average Price:", sum(prices) / len(prices))

print("\nCategory-wise Average Price")
for cat, price_list in categories.items():
    avg_price = sum(price_list) / len(price_list)
    print(cat, ":", round(avg_price, 2))

print("\nHigh Demand Products (based on rating count):")
for product in high_demand:
    print("-", product)
