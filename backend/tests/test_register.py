import pytest
from app import app, get_db_connection
import os

test_url = f"https://127.0.0.1:5000/register"

@pytest.fixture
def client():
    os.environ["FLASK_ENV"] = "testing"  # Set testing mode
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def setup_database():
    # Set up a fresh test database before each test
    with get_db_connection() as conn:
        conn.execute("DROP TABLE IF EXISTS users")
        conn.execute("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                first_name TEXT,
                last_name TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                is_active INTEGER DEFAULT 1
            )
        """)
        conn.commit()

# Test successful registration
def test_register_success(client, setup_database):
    payload = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword",
        "first_name": "Test",
        "last_name": "User"
    }

    response = client.post(test_url, json=payload)
    assert response.status_code == 201
    assert response.json["message"] == "User registered successfully!"

    # Verify the user exists in the database
    with get_db_connection() as conn:
        user = conn.execute("SELECT * FROM users WHERE username = ?", ("testuser",)).fetchone()
        assert user is not None
        assert user["email"] == "test@example.com"

# Test missing fields
def test_register_missing_fields(client, setup_database):
    payload = {
        "username": "",
        "email": "test@example.com",
        "password": "testpassword"
    }

    response = client.post(test_url, json=payload)
    assert response.status_code == 400
    assert "User name, Email, and Password are required" in response.json["error"]

# Test duplicate username
def test_register_duplicate_username(client, setup_database):
    payload = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword",
        "first_name": "Test",
        "last_name": "User"
    }

    # First registration
    client.post(test_url, json=payload)

    # Duplicate registration
    response = client.post(test_url, json=payload)
    assert response.status_code == 400
    assert "Username or email already exists" in response.json["error"]
