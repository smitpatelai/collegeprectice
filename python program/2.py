import requests

url = requests.get("https://isro.vercel.app/api/spacecrafts")

response = url.json()

print(response["spacecrafts"][0]["name"])
print(response["spacecrafts"][3]["name"])
print(response["spacecrafts"][111]["name"])
print(response["spacecrafts"][86]["name"])