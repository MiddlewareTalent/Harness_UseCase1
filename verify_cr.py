import requests, json, sys

cr_number = input("Enter the CR number to validate: ")

url = f"https://dev228482.service-now.com/api/now/table/change_request?sysparm_query=number={cr_number}&sysparm_limit=1"
res = requests.get(url, auth=("admin", "Gb2NQv*V7pw!"))

if res.status_code == 200:
    result = res.json()["result"][0]
    if result["state"] == "5":  # 5 = Implemented
        print(f"✅ CR '{cr_number}' is in Implemented state.")
        sys.exit(0)
    else:
        print(f"❌ CR '{cr_number}' is NOT in Implemented state. State: {result['state']}")
        sys.exit(1)
else:
    print("❌ Failed to fetch CR info")
    sys.exit(1)
