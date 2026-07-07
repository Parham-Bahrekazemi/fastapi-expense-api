from fastapi import FastAPI, status, HTTPException, Path, Depends
from schemas import (
    ExpenseCreateSchema,
    ExpenseUpdateSchema,
    ExpenseResponseScehema,
    TotalExpensesResponseScehema,
    UserCreateSchema,
)
from typing import List
from contextlib import asynccontextmanager
from database import engine, Base, get_db, User, Expense

from sqlalchemy.orm import Session


FILE_NAME = "expenses.json"


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("starting the application")
    Base.metadata.create_all(bind=engine)
    yield
    print("shuting down the application")


app = FastAPI(lifespan=lifespan)


@app.get("/")
def root():
    return {"message": "hello world"}


@app.get(
    "/users",
    status_code=status.HTTP_200_OK,
)
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


@app.post(
    "/users",
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    user_create_schema: UserCreateSchema,
    db: Session = Depends(get_db),
):
    user = User(name=user_create_schema.name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.get(
    "/users/{user_id}/expenses",
    status_code=status.HTTP_200_OK,
    response_model=List[ExpenseResponseScehema],
)
def get_expenses(
    user_id: int,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    expenses = db.query(Expense).filter(Expense.user_id == user_id).all()

    return expenses


@app.get(
    "/users/{user_id}/expenses/{expense_id}",
    status_code=status.HTTP_200_OK,
    response_model=ExpenseResponseScehema,
)
def get_expense(
    user_id: int,
    expense_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    expense = (
        db.query(Expense)
        .filter(
            Expense.user_id == user_id,
            Expense.id == expense_id,
        )
        .first()
    )

    if expense is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found",
        )

    return expense


@app.post(
    "/users/{user_id}/expenses",
    status_code=status.HTTP_201_CREATED,
    response_model=ExpenseResponseScehema,
)
def create_expenses(
    user_id: int,
    expense_create_schema: ExpenseCreateSchema,
    db: Session = Depends(get_db),
):

    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    expense = Expense(
        description=expense_create_schema.description,
        amount=expense_create_schema.amount,
        user_id=user_id,
    )
    db.add(expense)
    db.commit()
    db.refresh(expense)

    return expense


@app.put(
    "/users/{user_id}/expenses/{expense_id}",
    status_code=status.HTTP_200_OK,
    response_model=ExpenseResponseScehema,
)
def update_expense(
    user_id: int,
    expense_id: int = Path(..., ge=1),
    expense_update_schema: ExpenseUpdateSchema = ...,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    expense = (
        db.query(Expense)
        .filter(
            Expense.user_id == user_id,
            Expense.id == expense_id,
        )
        .first()
    )

    if expense is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found",
        )

    if expense_update_schema.description is not None:
        expense.description = expense_update_schema.description

    if expense_update_schema.amount is not None:
        expense.amount = expense_update_schema.amount

    db.commit()
    db.refresh(expense)

    return expense


@app.delete(
    "/users/{user_id}/expenses/{expense_id}",
    status_code=status.HTTP_200_OK,
)
def delete_expense(
    user_id: int,
    expense_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    expense = (
        db.query(Expense)
        .filter(
            Expense.user_id == user_id,
            Expense.id == expense_id,
        )
        .first()
    )

    if expense is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found",
        )

    db.delete(expense)
    db.commit()

    return {"message": f"Expense with id {expense_id} deleted successfully."}


@app.get(
    "/users/{user_id}/total_expenses",
    response_model=TotalExpensesResponseScehema,
    status_code=status.HTTP_200_OK,
)
def get_total_expenses(
    user_id: int,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    expenses = db.query(Expense).filter(Expense.user_id == user_id).all()

    total = sum(expense.amount for expense in expenses)

    return {
        "expenses_count": len(expenses),
        "total_expenses": total,
    }
