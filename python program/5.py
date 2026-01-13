import requests

userinput = input("Enter Country Name: ")

response = requests.get(
    f"http://universities.hipolabs.com/search?country={userinput}"
).json()

if len(response) == 0:
    print("No universities found.")
else:
    i = 0
    while i < len(response):
        print(response[i]["name"])
        i += 1
