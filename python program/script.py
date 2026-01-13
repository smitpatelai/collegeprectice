import requests


url = requests.get("https://api.tvmaze.com/search/shows?q=hello")
response = url.json()
print(response)

#basic
print("Length: ", len(response))
print("keys:", response[0].keys())

print("First Show: ", response[0]["show"]["name"])
print("First Show Language:", response[0]["show"]["language"])

#Last name
print("Last Show Name: ", response[-1]["show"]["name"])

#all data
# for i in response:
#   print("NAME: ", i["show"]["name"]), "Language: ", i["show"]["language"]


# for i in range(0, len(response)):
#   print("NAME:",response[i]["show"]["name"] , "LANGUAGE",response[i]["show"]["language"])

for i in response:
    for j in i["show"]["genres"]:
       print("NAME:",i["show"]["name"],"Genres:",j)