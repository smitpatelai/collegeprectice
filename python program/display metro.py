import requests

url = "https://api.tfl.gov.uk/Line/Mode/tube/Status"

lines = requests.get(url).json()

for line in lines:
    status = line["lineStatuses"][0]
    print("METRO STATUS REPORT =================")
    print("Line Name          :", line["name"])
    print("Current Status     :", status["statusSeverityDescription"])
    print("Severity Level     :", status["statusSeverity"])
    print("Reason Description :", status.get("reason", "No reason"))
    print("Line Identifier    :", line["id"])
    print("-" * 40)
