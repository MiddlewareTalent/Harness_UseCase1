import subprocess
import smtplib
import json
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# === Git Metadata ===
def get_git_info():
    def safe_run(cmd, fallback):
        try:
            output = subprocess.check_output(cmd, shell=True, text=True).strip()
            return output if output else fallback
        except Exception:
            return fallback

    author = safe_run("git log -1 --pretty=format:'%an'", "unknown").strip("'")
    commit_msg = safe_run("git log -1 --pretty=format:'%s'", "No commit message")
    branch = safe_run("git rev-parse --abbrev-ref HEAD", "unknown")
    commit_hash = safe_run("git rev-parse --short HEAD", "unknown")

    return author, commit_msg, branch, commit_hash

author, commit_msg, branch, commit_hash = get_git_info()

# === Load ServiceNow CR Number ===
cr_number = "UNKNOWN"
if os.path.exists("cr_info.json"):
    try:
        with open("cr_info.json", "r") as f:
            cr_data = json.load(f)
            cr_number = cr_data.get("number", "UNKNOWN")
    except Exception as e:
        print(f"[❌] Failed to load CR number: {e}")

# === Config ===
NGROK_URL = "https://bd3c-136-232-205-158.ngrok-free.app"
GITHUB_REPO_URL = "https://github.com/MiddlewareTalent/Harness_UseCase1.git"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL = "yaswanthkumarch2001@gmail.com"
PASSWORD = "uqjc bszf djfw bsor"
TO_EMAIL = "Raviteja@middlewaretalents.com"

# === Email Setup ===
msg = MIMEMultipart("alternative")
msg["Subject"] = "🛡️ Deployment Approval Request – Harness Use Case 1"
msg["From"] = EMAIL
msg["To"] = TO_EMAIL

approve_link = f"{NGROK_URL}/approve"
reject_link = f"{NGROK_URL}/reject"

servicenow_note = f"""✅ ServiceNow Change Request <strong>{cr_number}</strong> has been <strong>approved</strong> and passed internal audit.
<br>You're now requested to approve or reject the final production deployment."""

# === Email HTML Body ===
html = f"""
<html>
  <body style="font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 20px; color: #333;">
    <div style="max-width: 600px; margin: auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
      <h2 style="color: #2c3e50;">🚀 Deployment Approval Required</h2>
      <p><strong>Environment:</strong> <span style="color: #2980b9;">Production</span></p>
      <p><strong>Triggered By:</strong> {author}</p>
      <p><strong>Branch:</strong> <code>{branch}</code></p>
      <p><strong>Commit:</strong> {commit_msg} <code>({commit_hash})</code></p>

      <hr style="margin: 20px 0;">
      <p style="font-size: 16px;">{servicenow_note}</p>


      <hr style="margin: 30px 0;">
      <p><strong>🔗 GitHub Repository:</strong><br>
        <a href="{GITHUB_REPO_URL}" style="color: #007bff;">{GITHUB_REPO_URL}</a>
      </p>

      <p style="font-size: 12px; color: gray; margin-top: 40px;">This is an automated approval request from the Harness CI/CD pipeline.</p>
    </div>
  </body>
</html>
"""

msg.attach(MIMEText(html, "html"))

# === Send Email ===
try:
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL, PASSWORD)
        server.sendmail(EMAIL, TO_EMAIL, msg.as_string())
    print("📧 Approval email sent successfully.")
except Exception as e:
    print(f"❌ Failed to send email: {e}")
