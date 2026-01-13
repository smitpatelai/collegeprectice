import requests

url = requests.get("https://isro.vercel.app/api/launchers")

response = url.json()

print(response["launchers"][0]["id"])
print(response["launchers"][3]["id"])
print(response["launchers"][10]["id"])
print(response["launchers"][8]["id"])