from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import threading
import time

app = Flask(__name__)

reminders = []
notifications = []

def reminder_worker():
    while True:
        now = datetime.now()
        due = []
        for r in reminders:
            if r['time'] <= now and not r['notified']:
                notifications.append({
                    'message': r['message'],
                    'time': now.isoformat()
                })
                r['notified'] = True
                due.append(r)
        time.sleep(10)

@app.route('/api/reminders', methods=['POST'])
def add_reminder():
    data = request.json
    try:
        reminder_time = datetime.fromisoformat(data['time'])
        reminder = {
            'id': len(reminders) + 1,
            'message': data['message'],
            'time': reminder_time,
            'notified': False
        }
        reminders.append(reminder)
        return jsonify({'status': 'success', 'reminder': reminder}), 201
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/api/reminders', methods=['GET'])
def get_reminders():
    return jsonify(reminders)

@app.route('/api/notifications', methods=['GET'])
def get_notifications():
    return jsonify(notifications)

if __name__ == '__main__':
    t = threading.Thread(target=reminder_worker, daemon=True)
    t.start()
    app.run(host='0.0.0.0', port=5000)