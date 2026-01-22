import requests

url = "https://api.openbrewerydb.org/v1/breweries"

response = requests.get(url).json()
brewery = response[0]

print("================ BREWERY INFORMATION REPORT =================\n")

print("Brewery Name     :", brewery.get("name", "N/A"))
print("Brewery Type     :", brewery.get("brewery_type", "N/A"))
print("City             :", brewery.get("city", "N/A"))
print("Country          :", brewery.get("country", "N/A"))
print("Website URL      :", brewery.get("website_url", "N/A"))

print("\n================ END OF RECORD ============================")
