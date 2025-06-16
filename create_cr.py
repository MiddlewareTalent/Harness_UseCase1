import requests, json

url = "https://dev228482.service-now.com/api/now/table/change_request"
auth = ("admin", "Gb2NQv*V7pw!")  # Replace with secrets

payload = {
    "short_description": "CI Pipeline Triggered Change",
    "description": "Auto-created by Harness pipeline",
    "category": "Software",
    "state": "5",  # 5 = Implement
    "approval": "approved"
}

headers = {"Content-Type": "application/json", "Accept": "application/json"}
res = requests.post(url, auth=auth, headers=headers, json=payload)

if res.status_code == 201:
    result = res.json()["result"]
    print(f"CR created: {result['number']}")
    with open("cr_info.json", "w") as f:
        json.dump({"number": result["number"]}, f)
else:
    print("Failed to create CR", res.text)
