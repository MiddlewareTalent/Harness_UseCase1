import os, requests

cr_number = os.getenv("CR_NUMBER")
if not cr_number:
    print("❌ CR_NUMBER env var is missing.")
    exit(1)

res = requests.get(
    f"https://dev228482.service-now.com/api/now/table/change_request?sysparm_query=number={cr_number}&sysparm_limit=1",
    auth=("admin", "your_password")
)

if res.status_code == 200:
    cr = res.json()["result"][0]
    if cr["state"] == "5":
        print(f"✅ CR {cr_number} is in Implemented state.")
        exit(0)
    else:
        print(f"❌ CR {cr_number} is NOT in Implemented state.")
        exit(1)
else:
    print("❌ Failed to fetch CR info.")
    exit(1)
