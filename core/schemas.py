from pydantic import BaseModel, Field


class ExpenseCreateSchema(BaseModel):
    description: str
    amount: float = Field(gt=0)


class ExpenseUpdateSchema(BaseModel):
    description: str | None = None
    amount: float | None = Field(default=None, gt=0)


class ExpenseResponseScehema(BaseModel):
    ID: int
    description: str
    amount: float


class TotalExpensesResponseScehema(BaseModel):
    expenses_count: int
    total_expenses: float
