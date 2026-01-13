import requests


url = "https://fakestoreapi.com/products"

products = requests.get(url).json()

for product in products:
    print("Product Title     :", product["title"])
    print("Category          :", product["category"])
    print("Price             :", product["price"])
    print("Rating Score      :", product["rating"]["rate"])
    print("Product ID        :", product["id"])
    print("-" * 40)
