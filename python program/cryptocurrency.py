import requests

url = "https://api.coingecko.com/api/v3/coins/markets"
params = {
    "vs_currency": "usd",
    "order": "market_cap_desc",
    "per_page": 5,
    "page": 1
}

data = requests.get(url, params=params).json()

# 1. Print crypto market data
print("Cryptocurrency Market Data:")
for coin in data:
    print(coin["name"],
          "Price:", coin["current_price"],
          "Market Cap:", coin["market_cap"],
          "24h Change:", coin["price_change_percentage_24h"])

# Take first coin record
first_coin = data[0]

# 2. Total keys in one crypto record
print("\nTotal keys in one crypto record:")
print(len(first_coin))

# 3. Print all available keys
print("\nAll available keys:")
for key in first_coin:
    print(key)
