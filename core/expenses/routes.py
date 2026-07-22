from fastapi import APIRouter, Path, Depends, HTTPException, status
from typing import List

from sqlalchemy.orm import Session

from app.database import get_db
from auth.dependencies import get_current_user

from users.model import UserModel
from expenses.model import ExpenseModel

from expenses.schemas import (
    ExpenseCreateSchema,
    ExpenseUpdateSchema,
    ExpenseResponseScehema,
)


router = APIRouter(tags=["Expenses"], prefix="/user")


@router.get(
    "/expenses",
    status_code=status.HTTP_200_OK,
    response_model=List[ExpenseResponseScehema],
)
def get_expenses(
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    expenses = (
        db.query(ExpenseModel).filter(ExpenseModel.user_id == current_user.id).all()
    )

    return expenses


@router.post(
    "/expenses",
    status_code=status.HTTP_201_CREATED,
    response_model=ExpenseResponseScehema,
)
def create_expense(
    expense_create_schema: ExpenseCreateSchema,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    expense = ExpenseModel(
        description=expense_create_schema.description,
        amount=expense_create_schema.amount,
        user_id=current_user.id,
    )

    db.add(expense)
    db.commit()
    db.refresh(expense)

    return expense


@router.put(
    "/expenses/{expense_id}",
    response_model=ExpenseResponseScehema,
)
def update_expense(
    expense_id: int = Path(..., ge=1),
    expense_update_schema: ExpenseUpdateSchema = ...,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    expense = (
        db.query(ExpenseModel)
        .filter(
            ExpenseModel.id == expense_id,
            ExpenseModel.user_id == current_user.id,
        )
        .first()
    )

    if expense is None:
        raise HTTPException(
            status_code=404,
            detail="Expense not found",
        )

    if expense_update_schema.description is not None:
        expense.description = expense_update_schema.description

    if expense_update_schema.amount is not None:
        expense.amount = expense_update_schema.amount

    db.commit()
    db.refresh(expense)

    return expense


@router.delete(
    "/expenses/{expense_id}",
    status_code=status.HTTP_200_OK,
)
def delete_expense(
    expense_id: int = Path(..., ge=1),
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    expense = (
        db.query(ExpenseModel)
        .filter(
            ExpenseModel.id == expense_id,
            ExpenseModel.user_id == current_user.id,
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
