import sqlite3
from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Initialize DB
def init_db():
    conn = sqlite3.connect('sensor_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            temperature REAL,
            humidity REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/sensor-data', methods=['POST'])
def sensor_data():
    data = request.get_json()
    print(f"Received data: {data}")

    temp = data.get('temperature')
    hum = data.get('humidity')

    conn = sqlite3.connect('sensor_data.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO sensor_data (temperature, humidity) VALUES (?, ?)', (temp, hum))
    conn.commit()
    conn.close()

    return jsonify({'status': 'saved'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
