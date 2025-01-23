# WealthWise

WealthWise is a comprehensive personal and business finance tool designed to track expenses, manage budgets, and more.

## 🛠️ Local Development and Deployment Instructions

### Clone the Repository

```terminal
git clone https://github.com/your-repo.git
cd your-repo
```

### Create a Virtual Environment

```terminal
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Install Dependencies

```terminal
pip install -r requirements.txt
```

### Create a local version of the database

```terminal
python ./backend/database.py
```

### Run the Application

```terminal
cd backend
python ./backend/app.py
```

### Adding a User Via the API

```powershell
Invoke-WebRequest -Uri http://127.0.0.1:5000/register `
    -Method POST `
    -ContentType "application/json" `
    -Body '{"username": "testuser", "email": "test@example.com", "password": "securepassword", "first_name": "Test", "last_name": "User"}'
```

```bash
curl -X POST http://127.0.0.1:5000/register \
-H "Content-Type: application/json" \
-d '{"username": "testuser", "email": "test@example.com", "password": "securepassword", "first_name": "Test", "last_name": "User"}'
```
