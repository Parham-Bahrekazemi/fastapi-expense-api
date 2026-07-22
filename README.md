# FastAPI Expense API

A production-ready REST API built with **FastAPI** for managing users and expenses.

The project demonstrates modern backend development practices including:

- JWT Authentication
- Refresh Token Authentication
- Role-Based Access Control (RBAC)
- SQLAlchemy ORM
- Dependency Injection
- Password Hashing (bcrypt)
- User Ownership Validation
- Admin & Super Admin Authorization
- SQLite Database

---

## Features

### Authentication

- User Registration
- User Login
- JWT Access Token
- JWT Refresh Token
- Password Hashing using bcrypt
- Protected Endpoints

---

### Authorization

Three different roles are supported:

- User
- Admin
- Super Admin

Permission system includes:

- Users can manage only their own expenses.
- Admins can view all users.
- Admins can delete only normal users.
- Super Admin can promote users to admins.
- Super Admin can revoke admin permissions.
- Super Admin accounts cannot be deleted.
- Admins cannot delete themselves.

---

### Expense Management

Authenticated users can:

- Create expenses
- View their own expenses
- Update their own expenses
- Delete their own expenses

Ownership validation prevents users from accessing other users' expenses.

---

## Tech Stack

- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- JWT (PyJWT)
- Passlib (bcrypt)

---

## Project Structure

```
app/
    config.py
    database.py

auth/
    dependencies.py
    jwt.py
    permissions.py

users/
    model.py
    routes.py
    schemas.py

expenses/
    model.py
    routes.py
    schemas.py

super_admin/
    routes.py

scripts/
    create_super_admin.py
```

---

## API Endpoints

### Authentication

| Method | Endpoint |
|---------|----------|
| POST | /auth/register |
| POST | /auth/login |
| POST | /auth/refresh |

---

### Users

| Method | Endpoint |
|---------|----------|
| GET | /auth/users |
| GET | /auth/users/{id} |
| DELETE | /auth/users/{id} |

---

### Super Admin

| Method | Endpoint |
|---------|----------|
| PATCH | /super-admin/users/{id}/make-admin |
| PATCH | /super-admin/users/{id}/revoke-admin |

---

### Expenses

| Method | Endpoint |
|---------|----------|
| GET | /user/expenses |
| POST | /user/expenses |
| PUT | /user/expenses/{id} |
| DELETE | /user/expenses/{id} |

---

## Security

- JWT Access Tokens
- Refresh Tokens
- Password Hashing with bcrypt
- Role-Based Access Control
- Protected Routes
- User Ownership Validation

