import time, json, os

print("📥 Please enter the CR number in 'cr_input.json' file (format: {\"number\": \"CHG0030012\"})")
while not os.path.exists("cr_input.json"):
    print("⏳ Waiting for cr_input.json to be created...")
    time.sleep(10)

with open("cr_input.json", "r") as f:
    data = json.load(f)
    cr_number = data.get("number")

    if not cr_number:
        print("❌ CR number missing in cr_input.json")
        exit(1)

    with open("cr_env.sh", "w") as env_file:
        env_file.write(f'export CR_NUMBER="{cr_number}"\n')
    print(f"✅ Received CR number: {cr_number}")
