from fastapi import FastAPI, status, HTTPException, Path
from fastapi.responses import JSONResponse
import json
from schemas import (
    ExpenseCreateSchema,
    ExpenseUpdateSchema,
    ExpenseResponseScehema,
    TotalExpensesResponseScehema,
)
from typing import List

FILE_NAME = "expenses.json"


def load_expenses() -> list:
    with open(FILE_NAME, "r") as file:
        return json.load(file)


def save_expenses(expenses):
    with open(FILE_NAME, "w") as file:
        json.dump(expenses, file, indent=4)


app = FastAPI()


@app.get("/")
def root():
    return {"message": "hello world"}


@app.get(
    "/expenses",
    status_code=status.HTTP_200_OK,
    response_model=List[ExpenseResponseScehema],
)
def get_expenses():
    try:
        return load_expenses()
    except HTTPException as e:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e)


@app.get(
    "/expenses/{expense_id}",
    status_code=status.HTTP_200_OK,
    response_model=ExpenseResponseScehema,
)
def get_expense(expense_id: int = Path(..., ge=1)):
    try:
        expenses = load_expenses()
        for expense in expenses:
            if expense["ID"] == expense_id:
                return JSONResponse(
                    status_code=status.HTTP_200_OK,
                    content=expense,
                )
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Expense Not Found")
    except HTTPException as e:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)


@app.post(
    "/expenses",
    status_code=status.HTTP_201_CREATED,
    response_model=ExpenseResponseScehema,
)
def create_expenses(expense_create_schema: ExpenseCreateSchema):
    try:
        expenses = load_expenses()

        new_id = max((item["ID"] for item in expenses), default=0) + 1

        expense = {
            "ID": new_id,
            "description": expense_create_schema.description,
            "amount": expense_create_schema.amount,
        }

        expenses.append(expense)

        save_expenses(expenses)

        return expense
    except HTTPException as e:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)


@app.put(
    "/expenses/{expense_id}",
    status_code=status.HTTP_200_OK,
    response_model=ExpenseResponseScehema,
)
def update_expense(
    expense_update_schema: ExpenseUpdateSchema,
    expense_id: int = Path(..., ge=1),
):
    expenses = load_expenses()
    description = expense_update_schema.description
    amount = expense_update_schema.amount
    for expense in expenses:
        if expense["ID"] == expense_id:
            if description is not None:
                expense["description"] = description
            if amount is not None:
                expense["amount"] = amount
            save_expenses(expenses)
            return expense
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Expense Not Found"
    )


@app.delete("/expenses/{expense_id}", status_code=status.HTTP_200_OK)
def delete_expense(expense_id: int = Path(..., ge=1)):
    try:
        expenses = load_expenses()
        for expense in expenses:
            if expense["ID"] == expense_id:
                expenses.remove(expense)
                save_expenses(expenses)
                return JSONResponse(
                    content={
                        "message": f"Expense with ID {expense_id} deleted successfully."
                    },
                    status_code=status.HTTP_200_OK,
                )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Expense Not Found"
        )

    except HTTPException as e:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)


@app.get("/total_expenses", response_model=TotalExpensesResponseScehema)
def get_total_expenses():
    expenses = load_expenses()
    total = sum(expense["amount"] for expense in expenses)
    return {"expenses_count": len(expenses), "total_expenses": total}
