mydata ={
    "maharashtra":{"mumbai":{"city":"metro city","metro":"yes"},
        "population":"20 cr"},
            "gujarat": ["AHMEDABAD","SURAT","RAJKOT"],
                "rajasthan":["AJMER","JAISALMER",{"capital":"jaipur"},["MEWAD","RJ","INR"]]

}

print(mydata.keys())

print(len(mydata))

print(mydata["maharashtra"]["mumbai"]["city"])

print(mydata["rajasthan"][2]["capital"])

print(mydata["gujarat"][2])

print(mydata["rajasthan"][3][1])

