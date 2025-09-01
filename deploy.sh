#!/bin/bash - demo



echo "📦 Installing Python dependencies....."
pip install requests --quiet

echo "📁 Checking log files in logs/ directory..."
ls -l logs/ || echo "⚠️ logs/ directory not found!"

echo "🚀 Starting Python script to send logs to Splunk..."

python3 <<EOF
import json
import requests
import glob
import os

# 🔐 Splunk credentials
SPLUNK_HEC_URL = "https://prd-p-idagf.splunkcloud.com:8088"
SPLUNK_HEC_TOKEN = "6e0ba98d-a308-4e56-bf0f-2bccb7b803ab"
SPLUNK_INDEX = "ravi-index"
SPLUNK_SOURCETYPE = "new_logs"

headers = {
    "Authorization": f"Splunk {SPLUNK_HEC_TOKEN}",
    "Content-Type": "application/json"
}

log_files = glob.glob("logs/new.log")

if not log_files:
    print("⚠️ No log files found in logs/ — skipping send.")
else:
    print(f"📂 Found log file(s): {log_files}")

for filepath in log_files:
    if os.path.getsize(filepath) == 0:
        print(f"⚠️ Skipping empty log file: {filepath}")
        continue

    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            payload = {
                "event": line,
                "sourcetype": SPLUNK_SOURCETYPE,
                "index": SPLUNK_INDEX,
                "source": os.path.basename(filepath)
            }
            print(f"📤 Sending from {os.path.basename(filepath)}: {line}")
            try:
                response = requests.post(
                    f"{SPLUNK_HEC_URL}/services/collector/event",
                    headers=headers,
                    data=json.dumps(payload),
                    timeout=10,
                    verify=False
                )
                if response.status_code == 200:
                    print(f"✅ Sent successfully")
                else:
                    print(f"❌ Error {response.status_code}: {response.text}")
            except Exception as e:
                print(f"❌ Exception while sending log: {e}")
EOF

echo "📧 Sending deployment success email..."

python3 <<EOF
import smtplib
from email.message import EmailMessage

# 📧 SMTP Config
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "eshwar.bashabathini88@gmail.com"
SMTP_PASSWORD = "rqob tobv xdeq pscr"
TO_EMAIL = "Raviteja@middlewaretalents.com"

msg = EmailMessage()
msg["Subject"] = "✅ Deployment Successful - Splunk Automation"
msg["From"] = SMTP_USERNAME
msg["To"] = TO_EMAIL
msg.set_content("🎉 Deployment to Splunk has completed successfully!\n\n logs were sent.\n\nRegards,\nHarness Automation Bot")

try:
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.send_message(msg)
        print("✅ Deployment success email sent!")
except Exception as e:
    print(f"❌ Failed to send success email: {e}")
EOF
