#a = "Twinkle"
#print(a)

# dict
#key - value pair
        #name:"twinkle"

# rules
    # 1. {}
    # 2. key - value pair
    # 3. if you want to access value , key is required

mydata = {
    "name": "twinkle",
    "exp":7
}
print(mydata["name"],mydata["exp"])


coviddata = {
    "Ahmedabad":3200,
    "Surat":2900,
    "Rajkot":1200
}
print(coviddata["Ahmedabad"])
print("Surat Cases:", coviddata["Surat"])
print("RajkotCases:", coviddata["Rajkot"])
print("AhmedabadCases:", coviddata["Ahmedabad"])

# key -- multiple value

# a = 10
# a = [10,20,30]

coviddata1 = {
    "Ahmedabad":[1200,1000,1000],
    "Surat":2900,
    "Rajkot":1200
}

print("Ahmedabad cases:", coviddata1["Ahmedabad"])
print("Ahmedabad death cases:",coviddata1["Ahmedabad"][1])
print("Ahmedabad recovered cases:",coviddata1["Ahmedabad"][2])

coviddata2 = {
    "Ahmedabad":[
    {
        "Date":"5 Jan",
        "Cases":[120,80,100]
    },
    {
        "Date":"6 Jan",
        "Cases":400,
    },
    {
        "Date":"7 Jan",
        "Cases":800
    }
    ]
}

print("Ahmedabad", coviddata2["Ahmedabad"][1]["Date"],"Cases:",coviddata2["Ahmedabad"][1]["Cases"])
print("Ahmedabad", coviddata2["Ahmedabad"][2]["Date"],"Cases:",coviddata2["Ahmedabad"][2]["Cases"])

print("Ahmedabad 5th jan - death cases",coviddata2["Ahmedabad"][0]["Cases"][1])
