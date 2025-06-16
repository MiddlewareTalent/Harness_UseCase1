import requests
import subprocess
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# === ServiceNow Dev Instance ====
SNOW_INSTANCE = "https://dev228482.service-now.com"
USERNAME = "admin"
PASSWORD = "Gb2NQv*V7pw!"  # Use CyberArk or Harness secrets later for security

# === Email Configuration ===
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "yaswanthkumarch2001@gmail.com"      # Replace with your sender email
SENDER_PASSWORD = "uqjc bszf djfw bsor"            # Use app password or CyberArk
RECIPIENT_EMAIL = "Raviteja@middlewaretalents.com"

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
        print(f"[❌] Failed to fetch Git metadata: {e}")
        return {}

# === Send Notification Email ===
def send_email(cr_number, cr_url):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"[ServiceNow] New CR Created: {cr_number}"
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECIPIENT_EMAIL

    html = f"""
    <html>
      <body>
        <p>✅ A new Change Request <strong>{cr_number}</strong> has been created.<br>
           🔗 Click the button below to view it in ServiceNow:</p>
        <a href="{cr_url}" style="
            display: inline-block;
            padding: 10px 20px;
            background-color: #007bff;
            color: white;
            text-decoration: none;
            border-radius: 5px;">View Change Request</a>
      </body>
    </html>
    """
    msg.attach(MIMEText(html, "html"))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())
        print(f"[✅] Email sent to {RECIPIENT_EMAIL}")
    except Exception as e:
        print(f"[❌] Failed to send email: {e}")

# === Create CR in ServiceNow ===
def create_change_request(metadata):
    url = f"{SNOW_INSTANCE}/api/now/table/change_request"
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    payload = {
        "short_description": f"Deployment for {metadata['branch']} - {metadata['commit_msg']}",
        "description": f"Deployment triggered by GitHub user: {metadata['author']} ({metadata['email']})\n"
                       f"Commit ID: {metadata['commit_id']}\nBranch: {metadata['branch']}",
        "category": "Software",
        "type": "normal",
        "risk": "low",
        "assignment_group": "Change Management",  # Optional: prefill assignment group
        "state": "New"
    }

    response = requests.post(url, auth=(USERNAME, PASSWORD), headers=headers, json=payload)

    if response.status_code == 201:
        data = response.json()["result"]
        cr_number = data["number"]
        sys_id = data["sys_id"]
        print(f"[✅] CR created: {cr_number} (sys_id: {sys_id})")

        # Save locally for future use
        with open("cr_info.json", "w") as f:
            json.dump({"sys_id": sys_id, "number": cr_number}, f)

        # Generate CR link and send email
        cr_link = f"{SNOW_INSTANCE}/nav_to.do?uri=change_request.do?sys_id={sys_id}"
        send_email(cr_number, cr_link)

    else:
        print(f"[❌] Failed to create CR: {response.status_code}\n{response.text}")

if __name__ == "__main__":
    metadata = get_git_metadata()
    if metadata:
        create_change_request(metadata)
