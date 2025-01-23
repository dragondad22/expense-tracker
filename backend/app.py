import sqlite3
from flask import Flask, request, jsonify
from flask_talisman import Talisman
from flask_cors import CORS
import bcrypt


app = Flask(__name__)

# Forces https 
Talisman(app)

# Enables cross orign scripting
CORS(app)

# Gets the connection to the WealthWise database
def get_db_connection():
    try:
        conn = sqlite3.connect('wealthwise.db')
        conn.row_factory = sqlite3.Row  # Enables dictionary-like access to rows
        return conn
    except sqlite3.Error as e:
        # Log the error and raise an exception
        print(f"Database connection failed: {str(e)}")
        raise RuntimeError("Failed to connect to the database.")


@app.route("/")
def hello_world():
    return "Welcome to WealthWise"


@app.route('/register', methods=['Post'])
def register():
    data = request.get_json()

    # Extract user data from request
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    first_name = data.get('first_name')
    last_name = data.get('last_name')

    # Hash the user password before storing it
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Verify required fields are entered.
    if not username or not email or not password:
        return jsonify({"error": "User name, Email, and Password are required to continue"}), 400

    try:
        # Use 'with' to ensure the connection is properly closed
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''
                INSERT INTO users (username, email, password, first_name, last_name, created_at, is_active)
                VALUES (?, ?, ?, ?, ?, datetime(), 1)
                ''',
                (username, email, hashed_password, first_name, last_name)
            )
            conn.commit()

        return jsonify({"message": "User registered successfully!"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Username or email already exists"}), 400
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


@app.route("/user/<username>")
def user_profile(username):
    return f"Welcome, {username}!"


if __name__ == "__main__":
    app.run(debug=True)
