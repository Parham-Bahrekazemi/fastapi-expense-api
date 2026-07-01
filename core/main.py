from fastapi import FastAPI, status, HTTPException, Path
from fastapi.responses import JSONResponse
import json

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


@app.get("/expenses", status_code=status.HTTP_200_OK)
def get_expenses():
    try:
        return load_expenses()
    except HTTPException as e:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e)


@app.get("/expenses/{expense_id}", status_code=status.HTTP_200_OK)
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


@app.post("/expenses", status_code=status.HTTP_201_CREATED)
def create_expenses(description: str, amount: float):
    try:
        expenses = load_expenses()

        new_id = max((item["ID"] for item in expenses), default=0) + 1

        expense = {
            "ID": new_id,
            "description": description,
            "amount": amount,
        }

        expenses.append(expense)

        save_expenses(expenses)

        return expense
    except HTTPException as e:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)


@app.put("/expenses/{expense_id}", status_code=status.HTTP_200_OK)
def update_expense(
    expense_id: int = Path(..., ge=1), description: str = None, amount: float = None
):
    expenses = load_expenses()
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


@app.get("/total_expenses")
def get_total_expenses():
    expenses = load_expenses()
    total = sum(expense["amount"] for expense in expenses)
    return {"expenses_count": len(expenses), "total_expenses": total}
