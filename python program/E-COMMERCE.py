import requests


url = "https://fakestoreapi.com/products"
products = requests.get(url).json()


product = products[0]

# 1. Print total keys in one product
print("Total keys in one product:", len(product))

# 2. Print all key names
print("\nAll key names:")
for key in product.keys():
    print(key)

# 3. Identify numeric vs string keys
numeric_keys = []
string_keys = []

for key, value in product.items():
    if isinstance(value, (int, float)):
        numeric_keys.append(key)
    elif isinstance(value, str):
        string_keys.append(key)

print("\nNumeric keys:", numeric_keys)
print("String keys:", string_keys)
