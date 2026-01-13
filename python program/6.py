import requests

def load_data(no):
    url = requests.get(f"https://randomuser.me/api/?results={no}")
    response = url.json()
    return response

def search_user(users):
    found=False
    search_name = input("Enter User Name: ")
    for i in users:
        if search_name==i["name"]["first"]:
            print("User Found| NAME:",i["name"]["first"])
            found=True
            break
    else:
        print("User Not Found")
        return users



def main():
    number = int(input("Enter NO Of Users: "))
    response=load_data(number)
    print(response)
    users = response["results"]
    search_user(users)

main()