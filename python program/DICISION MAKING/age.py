#age = int(input("Enter Age:"))


# if age>18:
#     print("You are elligible")




# if age>=18:
#     print("You are elligible")
# else:
#     print("You are Not Elligible")




# if age>=18 and age<=58:
#     print("You can Work")
# elif age>58:
#     print("You are Retired")
# else:
#     print("You are Minor")

#nested if else
# admin login
id = "Admin@Infolabz"
password = "Admin"

id1 = input("Enter your ID: ")
pass1 = input("Enter your password: ")

if id1=="":
    if pass1=="":
        print("Please Fill All Details")
    else:
        print("Please Enter ID")
elif pass1=="":
    print("Please Enter Password")
elif id1==id:
    if pass1==password:
        print("Welcome Admin")
    else:
        print("Invalid Password")
elif pass1==password:
    if id1==id:
        print("Welcome Admin")
    else:
        print("Invalid ID")
else:
    print("Invalid Credentials")