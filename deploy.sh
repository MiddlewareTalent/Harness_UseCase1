#!/bin/bash

echo "📦 Installing Python dependencies...."
pip install requests --quiet

echo "📁 Checking log files in logs/ directory..."
ls -l logs/ || echo "⚠️ logs/ directory not found!"

echo "🚀 Starting Python script to send logs to Splunk..."

python3 <<EOF
import json
import requests
import glob
import os

# 🔐 Hardcoded Splunk credentials (use Harness secrets in production)
SPLUNK_HEC_URL = "https://prd-p-p4d4r.splunkcloud.com:8088"
SPLUNK_HEC_TOKEN = "2ba8def0-7c2d-46ae-876d-847e4f5b13c8"
SPLUNK_INDEX = "ravi-index"
SPLUNK_SOURCETYPE = "app_logs"

headers = {
    "Authorization": f"Splunk {SPLUNK_HEC_TOKEN}",
    "Content-Type": "application/json"
}

log_files = glob.glob("logs/app.log")

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
