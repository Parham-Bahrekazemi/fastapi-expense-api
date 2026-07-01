# FastAPI Expense API

A simple RESTful Expense Tracker API built with **FastAPI** for learning and practicing REST API development.

This project implements a complete CRUD API for managing expenses without using a database. Instead, expense data is persisted in a local JSON file, making it a lightweight and beginner-friendly example of FastAPI.

## Features

- Create a new expense
- Retrieve all expenses
- Retrieve a single expense by ID
- Update an existing expense
- Delete an expense
- Calculate the total amount of all expenses
- Automatic numeric ID generation
- JSON file persistence (no database required)
- Interactive API documentation with Swagger UI

## Tech Stack

- Python 3
- FastAPI
- Uvicorn
- JSON file storage

## Project Structure

```
fastapi-expense-api/
│
├── core/
│   ├── main.py
│   └── expenses.json
│
├── docs/
├── requirements.txt
├── README.md
└── LICENSE
```

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

Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the development server:

```bash
fastapi dev core/main.py
```

or

```bash
uvicorn core.main:app --reload
```

## API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | `/` | Welcome endpoint |
| GET | `/expenses` | Retrieve all expenses |
| GET | `/expenses/{id}` | Retrieve a single expense |
| POST | `/expenses` | Create a new expense |
| PUT | `/expenses/{id}` | Update an expense |
| DELETE | `/expenses/{id}` | Delete an expense |
| GET | `/total_expenses` | Get total expenses and count |

## API Documentation

After starting the server, FastAPI automatically provides interactive documentation:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Notes

- This project intentionally avoids using a database.
- Expense data is stored in `expenses.json`.
- IDs are generated automatically.
- Designed as a learning project for practicing FastAPI fundamentals.
