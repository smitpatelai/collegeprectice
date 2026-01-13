import requests

try:
    url = requests.get("https://disease.sh/v3/covid-19/countries",timeout=5)
    data = url.json()
    print(data)

    asia_countries = []
    europe_countries = []
    continents = []

    for i in data:
        name= i.get("country","UnKnown")
        continent = i.get("continent")

        if continents == "Asia":
            asia_countries.append(name)

except requests.exceptions.ConnectionError:
    print("Connection Error:")

except requests.exceptions.Timeout:
    print("Timeout Error:")

except requests.exceptions.HTTPError as err:
    print("HTTP Error occurred :", {err})

except ValueError:
    print("VALUE Error: API Returns Invalid JSON Data")

except Exception as e:
    print(f"Unknown Error: {e}")

