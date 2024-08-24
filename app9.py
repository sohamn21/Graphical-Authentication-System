from flask import Flask, render_template, request, jsonify
import sqlite3
import random
import os

app = Flask(__name__)

# Function to fetch icons associated with the provided Gmail address
def fetch_icons(gmail):
    try:
        conn = sqlite3.connect('login.db')
        cursor = conn.cursor()
        cursor.execute("SELECT icon1, icon2 FROM UserData WHERE gmail = ?", (gmail,))
        icons = cursor.fetchone()
        conn.close()
        return icons  # Return the icons in the correct order
    except Exception as e:
        print("Error fetching icons:", e)
        return None

# Function to generate random coordinates for fetched icons
def generate_coordinates():
    coordinates = []
    while len(coordinates) < 2:
        x = random.randint(0, 7)
        y = random.randint(0, 7)
        if (x, y) not in coordinates:
            coordinates.append((x, y))
    return coordinates

@app.route('/')
def signin_page():
    return render_template('signin.html')

# Route to handle the form submission for signing in
@app.route('/signin', methods=['POST'])
def signin():
    try:
        # Get the user's Gmail from the form submission
        gmail = request.form['gmail']
        print("Received Gmail:", gmail)  # Debugging statement

        # Fetch icons associated with the provided Gmail
        icons = fetch_icons(gmail)
        print("Fetched icons:", icons)  # Debugging statement

        # Generate random coordinates for fetched icons
        coordinates = generate_coordinates()
        print("Random positions for fetched icons:", coordinates)

        if icons:
            # Return the icons and their coordinates
            return jsonify({'status': 'success', 'icons': icons, 'coordinates': coordinates})
        else:
            return jsonify({'status': 'error', 'message': 'User not found. Please try again.'})
    except Exception as e:
        print("Error processing signin request:", e)
        return jsonify({'status': 'error', 'message': 'An error occurred during authentication.'})

if __name__ == '__main__':
    app.run(debug=True)