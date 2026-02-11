import requests
import matplotlib.pyplot as plt

url = requests.get("https://disease.sh/v3/covid-19/countries")
response = url.json()


cases = []
deaths = []
recovered = []
active = []
country =[]


response.sort(key=lambda x: x["cases"], reverse=True)

for i in response[:20]:
    cases.append(i["cases"])
    deaths.append(i["deaths"])
    recovered.append(i["recovered"])
    active.append(i["active"])
    country.append(i["country"])



#cases --->deaths
plt.scatter(cases, deaths,s=[i/300 for i in active],label=country,alpha=0.4)

for i , j in enumerate(country):
    plt.annotate(j,(cases[i],deaths[i]))

# plt.legend()
plt.show()

# top 20 ---->cases
