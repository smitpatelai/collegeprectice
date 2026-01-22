import requests

# API URL
url = "https://api.openbrewerydb.org/v1/breweries"

# Fetch data from API
response = requests.get(url)
data = response.json()

# Fetch one brewery record (first record)
brewery = data[0]

print("ONE BREWERY RECORD")
print("===================")
print(brewery)

# Count total keys
total_keys = len(brewery)
print("\nTOTAL KEYS:", total_keys)

# Print all key names using loop
print("\nKEY NAMES")
print("=========")
for key in brewery.keys():
    print(key)
