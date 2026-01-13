import requests

url = requests.get("https://disease.sh/v3/covid-19/countries")
response = url.json()

asia_countries = open("asia_countries.txt","w")
europe_cases = open("europe_cases.txt","w")
summary = open("summary.txt","w")

for i in response:
    name = i.get("country")
    continent = i.get("continent")
    cases = i.get("cases")
    deaths = i.get("deaths")
    recovered = i.get("recovered")

    if continent=="Asia":
        asia_countries.write(f"name: {name}\n")

    if continent=="Europe":
        europe_cases.write(f"name: {name}\n")

# summary
    summary.write(f"{name} | Cases: {cases}| Recoveres: {recovered}| Daths: {deaths}\n")
