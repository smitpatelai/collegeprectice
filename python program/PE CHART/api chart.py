import requests
import matplotlib.pyplot as plt

userin = input("Enter Country Name [e.g. USD/INR] : ")
url = requests.get(f"https://api.exchangerate-api.com/v4/latest/{userin}")
response = url.json()

country = []
price = []

for i,j in list(response["rates"].items())[:10]:
    country.append(i)
    price.append(j)

print(country)
print(price)

plt.plot(country,price,marker="o")
plt.xlabel("Country Name")
plt.ylabel("Price")
plt.title("Average Price")
plt.show()