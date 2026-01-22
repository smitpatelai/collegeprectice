import requests

# API URL
url = "https://openlibrary.org/subjects/science_fiction.json"

# Fetch data from API
response = requests.get(url)
data = response.json()

# Get one processed book record (first book)
book = data["works"][0]

print("PROCESSED BOOK RECORD ANALYSIS")
print("=" * 40)

# 1. Print total number of keys
print("Total number of keys:", len(book))

print("\nList of all key names:")
# 2. Print all key names
for key in book.keys():
    print("-", key)

print("\nDatatype of each key:")

# 3. Print datatype of every key
for key, value in book.items():
    print(f"{key} : {type(value)}")
