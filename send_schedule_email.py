import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# === Email Config ===
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL = "eshwar.bashabathini88@gmail.com"
PASSWORD = "rqob tobv xdeq pscr"  # App password
TO_EMAIL = "Raviteja@middlewaretalents.com"

# === ngrok URL ===
NGROK_URL = " https://a0ac3e6bc3c6.ngrok-free.app "
schedule_link = f"{NGROK_URL}/schedule_form"

# === Email Message ====
msg = MIMEMultipart("alternative")
msg["Subject"] = "📅 Schedule Deployment – Harness Splunk Pipeline"
msg["From"] = EMAIL
msg["To"] = TO_EMAIL

html = f"""
<html>
  <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
    <div style="max-width: 600px; background: white; padding: 20px; border-radius: 10px; margin: auto;">
      <h2 style="color: #2c3e50;">🛠️ Schedule Your Deployment</h2>
      <p>Please choose the date and time to schedule the deployment.</p>
      <p>
        <a href="{schedule_link}" style="display:inline-block; padding:12px 24px; background-color:#007bff; color:#fff; text-decoration:none; border-radius:6px;">
          📅 Click here to schedule
        </a>
      </p>
      <p style="font-size: 12px; color: gray; margin-top: 30px;">This email was sent automatically from the Harness CI/CD pipeline.</p>
    </div>
  </body>
</html>
"""

msg.attach(MIMEText(html, "html"))

# === Send Email ====
try:
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL, PASSWORD)
        server.sendmail(EMAIL, TO_EMAIL, msg.as_string())
    print("📧 Schedule email sent successfully.")
except Exception as e:
    print(f"❌ Failed to send schedule email: {e}")