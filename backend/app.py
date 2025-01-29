import sqlite3
from flask import Flask, request, jsonify
from flask_talisman import Talisman
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import bcrypt
import os


current_directory = os.getcwd()
db_path = os.path.abspath(f"{current_directory}\\wealthwise.db")


app = Flask(__name__)


# Only enforce HTTPS if not in testing mode
if os.getenv("FLASK_ENV") != "testing":
    Talisman(app)


# Enables cross orign scripting
CORS(app)


# Add a secret key for JWT
app.config["JWT_SECRET_KEY"] = "your_secret_key_here"
jwt = JWTManager(app)


# Gets the connection to the WealthWise database
def get_db_connection():
    try:
        # Check if the file exists
        print(db_path)
        if not os.path.exists(db_path):
            raise FileNotFoundError(f"Database file '{db_path}' does not exist.")

        conn = sqlite3.connect(db_path)
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


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    # Extract user data from request
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    try:
        # Check the user in the database
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            user = cursor.fetchone()

            if user is None:
                return jsonify({"error": "Invalid username or password"}), 401

            # Verify the password
            if not bcrypt.checkpw(password.encode('utf-8'), user["password"]):
                return jsonify({"error": "Invalid username or password"}), 401

            # Create a JWT token
            access_token = create_access_token(identity={"username": username})
            return jsonify({"access_token": access_token}), 200

    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True)
