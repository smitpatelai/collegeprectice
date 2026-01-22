mydata = [
    {
        "states": [
            "GUJARAT",
            "RAJASTHAN",
            {"PORTION": "WEST INDIA"},
            {"LANGUAGES": ["GUJARATI", "MARWADI", ["HINDI", "ENGLISH"]]}
        ]
    },
    {
        "CODES": {
            "GUJARAT": "GJ",
            "RAJASTHAN": "RJ"
        }
    },
    ["7.07 CR", "8.5 CR"]
]

main_keys = []

for item in mydata:
    if isinstance(item, dict):
        main_keys.extend(item.keys())

print("Total number of main keys:", len(main_keys))


print("Main keys are:")
for key in main_keys:
    print(key)

print(mydata[1]["CODES"]["GUJARAT"])

print(mydata[0]["states"][0])

print(mydata[0]["states"][3]["LANGUAGES"][1])

print(mydata[0]["states"][3]["LANGUAGES"][2][1])

print(mydata[0]["states"][2]["PORTION"])

print(mydata[2][0])
