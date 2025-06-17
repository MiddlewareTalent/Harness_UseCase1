from flask import Flask, request, jsonify, render_template_string
import os

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
@app.route('/schedule_form')
def schedule_form():
    return render_template_string('''
        <h2>Schedule Deployment</h2>
        <form method="POST" action="/submit_schedule">
            <label>Date (YYYY-MM-DD):</label><br>
            <input type="text" name="date" required /><br>
            <label>Time (HH:MM 24hr):</label><br>
            <input type="text" name="time" required /><br>
            <button type="submit">Submit</button>
        </form>
    ''')

@app.route('/submit_schedule', methods=['POST'])
def submit_schedule():
    date = request.form['date']
    time = request.form['time']
    schedule = f"{date} {time}"
    with open(SCHEDULE_FILE, "w") as f:
        f.write(schedule)
    return f"✅ Schedule received: {schedule}"

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
    app.run(port=5000)
