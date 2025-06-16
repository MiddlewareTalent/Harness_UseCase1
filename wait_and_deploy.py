import time
from datetime import datetime

scheduled_time = input("Enter deployment time (YYYY-MM-DD HH:MM): ")
scheduled_dt = datetime.strptime(scheduled_time, "%Y-%m-%d %H:%M")

print(f"🕒 Waiting until {scheduled_dt} to deploy...")

while datetime.now() < scheduled_dt:
    time.sleep(10)

print("🚀 Deployment started...")
# Simulate your deployment logic here
