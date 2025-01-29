import pytest
from app import app, get_db_connection
import os
import bcrypt

@pytest.fixture
def client():
    os.environ["FLASK_ENV"] = "testing"  # Set testing mode
    app.config["TESTING"] = True
    with app.test_client() as client:
        client.environ_base["wsgi.url_scheme"] = "https"
        yield client


@pytest.fixture
def setup_database():
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
        # Insert a test user
        conn.execute("""
            INSERT INTO users (username, email, password, first_name, last_name)
            VALUES ('testuser', 'test@example.com', ?, 'Test', 'User')
        """, (bcrypt.hashpw("testpassword".encode('utf-8'), bcrypt.gensalt()),))
        conn.commit()


def test_login_success(client, setup_database):
    payload = {"username": "testuser", "password": "testpassword"}
    response = client.post("/login", json=payload)
    assert response.status_code == 200
    assert "access_token" in response.json


def test_login_invalid_credentials(client, setup_database):
    payload = {"username": "testuser", "password": "wrongpassword"}
    response = client.post("/login", json=payload)
    assert response.status_code == 401
    assert response.json["error"] == "Invalid username or password"


def test_login_missing_fields(client):
    payload = {"username": "testuser"}
    response = client.post("/login", json=payload)
    assert response.status_code == 400
    assert response.json["error"] == "Username and password are required"
