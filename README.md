# FastAPI Expense API

A simple RESTful Expense Tracker API built with **FastAPI** for learning and practicing REST API development.

This project implements a complete CRUD API for managing users and their expenses using **SQLAlchemy ORM** with **SQLite**. It demonstrates database relationships, dependency injection, request validation, and RESTful API design.

---

## Features

- Create and manage users
- Create a new expense for a specific user
- Retrieve all expenses of a user
- Retrieve a single expense
- Update an existing expense
- Delete an expense
- Calculate the total amount of a user's expenses
- SQLAlchemy ORM integration
- SQLite database
- One-to-Many relationship (User → Expenses)
- Automatic database table creation
- Pydantic request validation
- Interactive API documentation with Swagger UI

---

## Tech Stack

- Python 3
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Uvicorn

---

## Project Structure

```text
fastapi-expense-api/
│
├── core/
│   ├── database.py
│   ├── main.py
│   ├── schemas.py
│   └── sqlite.db
│
├── docs/
│   └── database_diagram.png
│
├── requirements.txt
├── README.md
└── LICENSE
```

---

## Database Schema

The application contains two tables:

### Users

| Column | Type |
|---------|------|
| id | Integer |
| name | String |

### Expenses

| Column | Type |
|---------|------|
| id | Integer |
| user_id | Integer (Foreign Key) |
| description | String |
| amount | Float |

Relationship:

```text
User (1)
    │
    └───────────────< Expense (Many)
```

The database diagram is available in:

```
docs/database_diagram.png
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/<your-username>/fastapi-expense-api.git
```

Navigate to the project:

```bash
cd fastapi-expense-api
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment.

**Windows**

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Run the Development Server

```bash
fastapi dev core/main.py
```

or

```bash
uvicorn core.main:app --reload
```

---

## API Endpoints

### Users

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/users` | Retrieve all users |
| POST | `/users` | Create a new user |

### Expenses

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/users/{user_id}/expenses` | Retrieve all expenses of a user |
| GET | `/users/{user_id}/expenses/{expense_id}` | Retrieve a single expense |
| POST | `/users/{user_id}/expenses` | Create a new expense |
| PUT | `/users/{user_id}/expenses/{expense_id}` | Update an expense |
| DELETE | `/users/{user_id}/expenses/{expense_id}` | Delete an expense |
| GET | `/users/{user_id}/total_expenses` | Get total expenses and count |

---

## API Documentation

After starting the server, FastAPI automatically provides interactive documentation.

- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc

---

## Notes

- The application uses **SQLite** as its database.
- Database tables are created automatically on application startup.
- Expenses belong to a specific user through a **one-to-many relationship**.
- SQLAlchemy is used as the ORM for database interactions.
- This project is designed as a learning project for practicing FastAPI, SQLAlchemy, and REST API fundamentals.
