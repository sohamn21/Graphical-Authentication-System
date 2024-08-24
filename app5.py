from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

# SQLite database connection
conn = sqlite3.connect('login.db', check_same_thread=False)
cursor = conn.cursor()

# Create table if not exists
cursor.execute('''CREATE TABLE IF NOT EXISTS UserData (
                    id INTEGER PRIMARY KEY,
                    gmail TEXT,
                    icon1 TEXT,
                    icon2 TEXT
                )''')
conn.commit()

@app.route('/')
def index():
    return render_template('newlogin.html')

@app.route('/saveUserData', methods=['POST'])
def save_user_data():
    data = request.json

    # Extract data from the request
    gmail = data.get('gmail')
    icons = data.get('icons')

    # Check if both icons are selected
    if len(icons) != 2:
        return jsonify({'error': 'Please select 2 icons.'}), 400

    try:
        # Insert user data into the database
        cursor.execute('INSERT INTO UserData (gmail, icon1, icon2) VALUES (?, ?, ?)',
                       (gmail, icons[0], icons[1]))
        conn.commit()
        return jsonify({'message': 'Data saved successfully!'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
