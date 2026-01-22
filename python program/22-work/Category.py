mydata = {
        "category":[{"A":"FIRST","package":{"data":"2lacs"}},
            {"B":"Second","data":{"new":[100]}},
                {"C":"Third","Tests":[45,75,25]}]
}

all_keys = []

def extract_keys(d):
    for k, v in d.items():
        all_keys.append(k)
        if isinstance(v, dict):
            extract_keys(v)
        elif isinstance(v, list):
            for i in v:
                if isinstance(i, dict):
                    extract_keys(i)

extract_keys(mydata)
print("All Keys:", all_keys)

print("Total number of keys:", len(all_keys))

print("2lacs:", mydata["category"][0]["package"]["data"])

print("25:", mydata["category"][2]["Tests"][-1])

print("100:", mydata["category"][1]["data"]["new"][0])