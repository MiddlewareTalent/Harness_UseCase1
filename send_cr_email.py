import subprocess
import smtplib
import json
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# === Git Metadata ===
def get_git_info():
    author = subprocess.getoutput("git log -1 --pretty=format:'%an'").strip("'")
    commit_msg = subprocess.getoutput("git log -1 --pretty=format:'%s'")
    branch = subprocess.getoutput("git rev-parse --abbrev-ref HEAD")
    commit_hash = subprocess.getoutput("git rev-parse --short HEAD")
    return author, commit_msg, branch, commit_hash

author, commit_msg, branch, commit_hash = get_git_info()

# === Config ===
NGROK_URL = "https://bd3c-136-232-205-158.ngrok-free.app"  # Your live public URL
GITHUB_REPO_URL = "https://github.com/MiddlewareTalent/Harness_Splunk_Automation_Approval.git"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL = "yaswanthkumarch2001@gmail.com"  # FROM
PASSWORD = "uqjc bszf djfw bsor"
TO_EMAIL = "Raviteja@middlewaretalents.com"  # TO

# === Email Setup ===
msg = MIMEMultipart("alternative")
msg["Subject"] = "📝 Enter CR Number – Harness Pipeline Input"
msg["From"] = EMAIL
msg["To"] = TO_EMAIL

# === CR Input Link ===
cr_input_link = f"{NGROK_URL}/cr_form"

# === Email HTML Body ===
html = f"""
<html>
  <body style="font-family: Arial, sans-serif; background-color: #f0f0f0; padding: 20px;">
    <div style="max-width: 600px; background: white; padding: 20px; margin: auto; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
      <h2 style="color: #2c3e50;">📥 Input Required: Enter CR Number</h2>
      <p><strong>Triggered By:</strong> {author}</p>
      <p><strong>Branch:</strong> <code>{branch}</code></p>
      <p><strong>Commit:</strong> {commit_msg} <code>({commit_hash})</code></p>

      <hr style="margin: 20px 0;">

      <p style="font-size: 16px;">Please click the button below to enter the ServiceNow Change Request Number to continue the deployment process.</p>

      <div style="margin: 20px 20px;">
        <a href="{cr_input_link}" style="background-color: #007bff; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; font-weight: bold;">🔗 Enter CR Number</a>
      </div>

      <hr style="margin: 30px 0;">
      <p><strong>📂 GitHub Repo:</strong><br>
        <a href="{GITHUB_REPO_URL}">{GITHUB_REPO_URL}</a></p>

      <p style="color: gray; font-size: 12px; margin-top: 40px;">
        This is an automated message from your Harness pipeline. Please do not reply.
      </p>
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
    print("📧 CR input email sent successfully.")
except Exception as e:
    print(f"❌ Failed to send email: {e}")
