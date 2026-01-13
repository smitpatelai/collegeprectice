import requests

userinput = input("Enter Country Name: ")
print(userinput)
print("you have entered",userinput)
print(f"you have entered {userinput}")

response=requests.get(f"http://universities.hipolabs.com/search?country={userinput}").json()

#print(f"Total Universities in {userinput}", len(response))
#print(response[0]["name"])

#for i in response:
 #   print(i["name"])

if len(response) == 0:
    print("No universities found.")
else:
    print(f"Total Universities in {userinput}: {len(response)}")
    print("First University:", response[0]["name"])


for i in range(len(response)):
    print(response[i]["name"])