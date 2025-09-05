# import requests
# import subprocess
# import json

# # === ServiceNow Dev Instance ====
# SNOW_INSTANCE = "https://dev293821.service-now.com/"
# USERNAME = "admin"
# PASSWORD = "N4kXM%bwcQ7*"  # Replace with secret manager like CyberArk later

# # === Fetch Git Commit Metadata ===
# def get_git_metadata():
#     try:
#         author = subprocess.check_output(["git", "log", "-1", "--pretty=format:%an"]).decode().strip()
#         email = subprocess.check_output(["git", "log", "-1", "--pretty=format:%ae"]).decode().strip()
#         commit_msg = subprocess.check_output(["git", "log", "-1", "--pretty=format:%s"]).decode().strip()
#         commit_id = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()
#         branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"]).decode().strip()
#         return {
#             "author": author,
#             "email": email,
#             "commit_msg": commit_msg,
#             "commit_id": commit_id,
#             "branch": branch
#         }
#     except Exception as e:
#         print(f"[❌] Failed to fetch Git metadata: {e}")
#         return {}

# # === Create CR in ServiceNow ===
# def create_change_request(metadata):
#     url = f"{SNOW_INSTANCE}/api/now/table/change_request"
#     headers = {"Content-Type": "application/json", "Accept": "application/json"}
#     payload = {
#         "short_description": f"Deployment for {metadata['branch']} - {metadata['commit_msg']}",
#         "description": f"Deployment triggered by GitHub user: {metadata['author']} ({metadata['email']})\n"
#                        f"Commit ID: {metadata['commit_id']}\nBranch: {metadata['branch']}",
#         "category": "Software",
#         "type": "normal",
#         "risk": "low",
#         "assignment_group": "Change Management",
#         "state": "New"
#     }

#     response = requests.post(url, auth=(USERNAME, PASSWORD), headers=headers, json=payload)

#     if response.status_code == 201:
#         data = response.json()["result"]
#         cr_number = data["number"]
#         sys_id = data["sys_id"]
#         print(f"[✅] CR created: {cr_number} (sys_id: {sys_id})")

#         # Save locally for future use
#         with open("cr_info.json", "w") as f:
#             json.dump({"sys_id": sys_id, "number": cr_number}, f)
#     else:
#         print(f"[❌] Failed to create CR: {response.status_code}\n{response.text}")

# if __name__ == "__main__":
#     metadata = get_git_metadata()
#     if metadata:
#         create_change_request(metadata)
import requests

import subprocess

import json

from datetime import datetime
 
# === ServiceNow Dev Instance ====

SNOW_INSTANCE = "https://dev293821.service-now.com"

USERNAME = "admin"

PASSWORD = "N4kXM%bwcQ7*"  # Use a secret manager in production

LOG_FILE = "change_request.log"
 
# ===== HARDCODED VARIABLES =====

PRIORITY = "3"

RISK = "2"

IMPACT = "2"
 
IMPLEMENTATION_PLAN = "Deploy updated Splunk logging integration via Harness CI pipeline."

JUSTIFICATION = "Enhances observability and improves log accuracy for production monitoring."

RISK_ANALYSIS = "Low risk as changes are limited to log format and routing. Impact is isolated to Splunk integration."

BACKOUT_PLAN = "Rollback to previous build artifact and disable new HEC configurations."

TEST_PLAN = "Test build in staging; validate log delivery to Splunk and ensure alerts are received."
 
ASSIGNMENT_GROUP = "Incident Management"

ASSIGNED_TO = None  # Can be set to a sys_id if required
 
# === Logging helper ===

def log(msg):

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"[{timestamp}] {msg}")

    with open(LOG_FILE, "a") as f:

        f.write(f"[{timestamp}] {msg}\n")
 
# === Fetch Git Commit Metadata ===

def get_git_metadata():

    try:

        author = subprocess.check_output(["git", "log", "-1", "--pretty=format:%an"]).decode().strip()

        email = subprocess.check_output(["git", "log", "-1", "--pretty=format:%ae"]).decode().strip()

        commit_msg = subprocess.check_output(["git", "log", "-1", "--pretty=format:%s"]).decode().strip()

        commit_id = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()

        branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"]).decode().strip()

        return {

            "author": author,

            "email": email,

            "commit_msg": commit_msg,

            "commit_id": commit_id,

            "branch": branch

        }

    except Exception as e:

        log(f"[❌] Failed to fetch Git metadata: {e}")

        return {}
 
# === Create CR in ServiceNow ===

def create_change_request(metadata):

    url = f"{SNOW_INSTANCE}/api/now/table/change_request"

    headers = {"Content-Type": "application/json", "Accept": "application/json"}
 
    payload = {

        "short_description": f"Automated CR from Harness CI Pipeline - {metadata.get('branch', 'N/A')}",

        "description": (

            f"Automated deployment for Splunk logging integration.\n"

            f"Triggered by: {metadata.get('author', '')} ({metadata.get('email', '')})\n"

            f"Commit ID: {metadata.get('commit_id', '')}\n"

            f"Branch: {metadata.get('branch', '')}"

        ),

        "category": "Software",

        "priority": PRIORITY,

        "risk": RISK,

        "impact": IMPACT,

        "state": "Assess",

        "assignment_group": ASSIGNMENT_GROUP,

        "assigned_to": ASSIGNED_TO,

        "implementation_plan": IMPLEMENTATION_PLAN,

        "justification": JUSTIFICATION,

        "u_risk_impact_analysis": RISK_ANALYSIS,

        "backout_plan": BACKOUT_PLAN,

        "test_plan": TEST_PLAN

    }
 
    log("🚀 Creating Change Request...")
 
    try:

        response = requests.post(url, auth=(USERNAME, PASSWORD), headers=headers, json=payload)

        response.raise_for_status()

        data = response.json().get("result", {})

        cr_number = data.get("number")

        sys_id = data.get("sys_id")
 
        if cr_number and sys_id:

            log(f"[✅] CR created: {cr_number} (sys_id: {sys_id})")

            with open("cr_info.json", "w") as f:

                json.dump({"sys_id": sys_id, "number": cr_number}, f)

        else:

            log(f"[❌] Unexpected response: {response.text}")
 
    except requests.exceptions.RequestException as e:

        log(f"[❌] Failed to create CR: {e}")

        log(f"Response: {getattr(e.response, 'text', '')}")
 
if __name__ == "__main__":

    metadata = get_git_metadata()

    if metadata:

        create_change_request(metadata)

 