import smtplib
from email.mime.text import MIMEText

link = "https://bd3c-136-232-205-158.ngrok-free.app/cr_form"  # Replace with your ngrok

body = f"""
Hi,

A new Change Request has been created.

👉 <a href="{link}">Click here to enter CR Number</a>

Thanks,
Harness CI/CD Bot
"""

msg = MIMEText(body, 'html')
msg['Subject'] = 'Enter CR Number for Validation'
msg['From'] = 'your@email.com'
msg['To'] = 'recipient@email.com'

with smtplib.SMTP('smtp.office365.com', 587) as server:
    server.starttls()
    server.login('your@email.com', 'your-app-password')
    server.send_message(msg)
