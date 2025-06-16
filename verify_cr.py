import requests, json, sys, os

# Read CR number from environment variable (set by Harness pipeline)
cr_number = os.getenv("CR_NUMBER")

if not cr_number:
    print("❌ CR_NUMBER environment variable not provided.")
    sys.exit(1)

url = f"https://dev228482.service-now.com/api/now/table/change_request?sysparm_query=number={cr_number}&sysparm_limit=1"
res = requests.get(url, auth=("admin", "Gb2NQv*V7pw!"))

if res.status_code == 200:
    result = res.json()["result"]
    if not result:
        print(f"❌ CR '{cr_number}' not found in ServiceNow.")
        sys.exit(1)

    cr = result[0]
    if cr["state"] == "5":  # 5 = Implemented
        print(f"✅ CR '{cr_number}' is in Implemented state.")
        sys.exit(0)
    else:
        print(f"❌ CR '{cr_number}' is NOT in Implemented state. State: {cr['state']}")
        sys.exit(1)
else:
    print("❌ Failed to fetch CR info")
    sys.exit(1)
