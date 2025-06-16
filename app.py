from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

cr_input = None
schedule_input = None

@app.route('/')
def index():
    return "ServiceNow Demo App Running..."

@app.route('/cr_form', methods=['GET'])
def cr_form():
    return render_template_string('''
        <h2>Enter CR Number to Validate</h2>
        <form method="POST" action="/submit_cr">
            <input type="text" name="cr_number" required />
            <button type="submit">Submit</button>
        </form>
    ''')

@app.route('/submit_cr', methods=['POST'])
def submit_cr():
    global cr_input
    cr_input = request.form['cr_number']
    return f"✅ CR Number '{cr_input}' received successfully."

@app.route('/get_cr_input', methods=['GET'])
def get_cr_input():
    return jsonify({"cr_number": cr_input})

@app.route('/schedule_form', methods=['GET'])
def schedule_form():
    return render_template_string('''
        <h2>Schedule Deployment</h2>
        <form method="POST" action="/submit_schedule">
            <label>Date (YYYY-MM-DD):</label><br>
            <input type="text" name="date" required /><br>
            <label>Time (HH:MM in 24hr):</label><br>
            <input type="text" name="time" required /><br>
            <button type="submit">Submit</button>
        </form>
    ''')

@app.route('/submit_schedule', methods=['POST'])
def submit_schedule():
    global schedule_input
    date = request.form['date']
    time = request.form['time']
    schedule_input = f"{date} {time}"
    return f"✅ Schedule received: {schedule_input}"

@app.route('/get_schedule', methods=['GET'])
def get_schedule():
    return jsonify({"schedule": schedule_input})

if __name__ == '__main__':
    app.run(port=5000)
