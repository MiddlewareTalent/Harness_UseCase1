from flask import Flask, request, jsonify, render_template_string
import os
from flask import Flask, request, render_template_string
from datetime import datetime
import pytz
app = Flask(__name__)

SCHEDULE_FILE = "schedule.txt"

@app.route('/')
def index():
    return "✅ ServiceNow Demo App Running..."

# === CR Input ===
@app.route('/cr_form')
def cr_form():
    return render_template_string('''
        <h2>Enter CR Number</h2>
        <form method="POST" action="/submit_cr">
            <input type="text" name="cr_number" required />
            <button type="submit">Submit</button>
        </form>
    ''')

@app.route('/submit_cr', methods=['POST'])
def submit_cr():
    cr_number = request.form['cr_number']
    with open("cr_number.txt", "w") as f:
        f.write(cr_number)
    return f"✅ CR Number '{cr_number}' received successfully."

@app.route('/get_cr_input')
def get_cr_input():
    if os.path.exists("cr_number.txt"):
        with open("cr_number.txt") as f:
            cr = f.read().strip()
        return jsonify({"cr_number": cr})
    return jsonify({"cr_number": None})

@app.route('/reset_cr_input', methods=['POST'])
def reset_cr_input():
    if os.path.exists("cr_number.txt"):
        os.remove("cr_number.txt")
    return jsonify({"message": "CR reset successful"})

# === Schedule Input ===
# @app.route('/schedule_form')
# def schedule_form():
#     return render_template_string('''
#         <h2>Schedule Deployment</h2>
#         <form method="POST" action="/submit_schedule">
#             <label>Date (YYYY-MM-DD):</label><br>
#             <input type="text" name="date" required /><br>
#             <label>Time (HH:MM 24hr):</label><br>
#             <input type="text" name="time" required /><br>
#             <button type="submit">Submit</button>
#         </form>
#     ''')

# @app.route('/submit_schedule', methods=['POST'])
# def submit_schedule():
#     date = request.form['date']
#     time = request.form['time']

#     schedule = f"{date} {time}"
#     with open(SCHEDULE_FILE, "w") as f:
#         f.write(schedule)
#     return f"✅ Schedule received: {schedule}"

from flask import Flask, request, render_template_string
from datetime import datetime
import pytz

@app.route('/schedule_form')
def schedule_form():
    return render_template_string('''
        <h2>📅 Schedule Deployment</h2>
        <form method="POST" action="/submit_schedule">
            <label>Date:</label><br>
            <input type="date" name="date" required /><br><br>

            <label>Time (24-hour):</label><br>
            <input type="time" name="time" required /><br><br>

            <label>Timezone:</label><br>
            <select name="timezone" required>
                <option value="UTC">UTC</option>
                <option value="Asia/Kolkata">Asia/Kolkata (IST)</option>
                <option value="US/Eastern">US/Eastern</option>
                <option value="US/Central">US/Central</option>
                <option value="US/Pacific">US/Pacific</option>
                <option value="Europe/London">Europe/London</option>
                <option value="Europe/Berlin">Europe/Berlin</option>
                <option value="Asia/Tokyo">Asia/Tokyo</option>
                <option value="Australia/Sydney">Australia/Sydney</option>
            </select><br><br>

            <button type="submit">✅ Submit</button>
        </form>
    ''')




@app.route('/submit_schedule', methods=['POST'])
def submit_schedule():
    date = request.form['date']
    time = request.form['time']
    timezone = request.form['timezone']

    try:
        # Combine date and time into datetime object in user's timezone
        naive_dt = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
        user_tz = pytz.timezone(timezone)
        user_dt = user_tz.localize(naive_dt)

        # Convert to UTC
        utc_dt = user_dt.astimezone(pytz.utc)

        # Save UTC time in strict format
        with open(SCHEDULE_FILE, "w") as f:
            f.write(utc_dt.strftime('%Y-%m-%d %H:%M'))

        return f"""
        ✅ Schedule received:<br>
        Original time ({timezone}): {user_dt.strftime('%Y-%m-%d %H:%M %Z')}<br>
        Converted to UTC: {utc_dt.strftime('%Y-%m-%d %H:%M %Z')}
        """

    except Exception as e:
        return f"❌ Error: {str(e)}"


@app.route('/get_schedule')
def get_schedule():
    if os.path.exists(SCHEDULE_FILE):
        with open(SCHEDULE_FILE) as f:
            schedule = f.read().strip()
        return jsonify({"schedule": schedule})
    return jsonify({"schedule": None})

@app.route('/reset_schedule', methods=['POST'])
def reset_schedule():
    if os.path.exists(SCHEDULE_FILE):
        os.remove(SCHEDULE_FILE)
    return jsonify({"status": "schedule reset"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
