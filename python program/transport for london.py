import requests

url = "https://api.tfl.gov.uk/Line/Mode/tube/Status"
data = requests.get(url).json()

# 1. Print metro line status
print("Metro Line Status:")
for line in data:
    print(line["name"], ":", line["lineStatuses"][0]["statusSeverityDescription"])

# Take first line record
first_line = data[0]

# 2. Print total keys
print("\nTotal keys in one line record:")
print(len(first_line))

# 3. Print all keys
print("\nAll available keys:")
for key in first_line:
    print(key)
