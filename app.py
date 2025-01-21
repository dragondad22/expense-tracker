import sqlite3
from flask import Flask, request, jsonify
import bcrypt


app = Flask(__name__)


# Gets the connection to the WealthWise database
def get_db_connection():
    conn = sqlite3.connect('wealthwise.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/register', methods=['Post'])
def register():
    data = request.get_json()

    # Extract user data from request
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')  # Store securely later
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    if not username or not email or not password:
        return jsonify({"error": "All fields required"}), 400

    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        # Insert the user into the database
        cursor.execute('''
            INSERT INTO users (username, email, password)
            VALUES (?, ?, ?)
        ''', (username, email, hashed_password))

        return jsonify({"message": "User registered successfully!"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Username or email already exists"}), 400
    finally:
        conn.commit()
        conn.close()

@app.route("/")
def hello_world():
    return "Hello World"


@app.route("/about")
def about():
    return "This is the about page."


@app.route("/user/<username>")
def user_profile(username):
    return f"Welcome, {username}!"


if __name__ == "__main__":
    app.run(debug=True)

