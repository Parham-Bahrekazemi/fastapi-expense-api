from pydantic import BaseModel, Field, ConfigDict


class ExpenseCreateSchema(BaseModel):
    description: str
    amount: float = Field(gt=0)


class ExpenseUpdateSchema(BaseModel):
    description: str | None = None
    amount: float | None = Field(default=None, gt=0)


class ExpenseResponseScehema(BaseModel):
    id: int
    description: str
    amount: float

    model_config = ConfigDict(from_attributes=True)


class TotalExpensesResponseScehema(BaseModel):
    expenses_count: int
    total_expenses: float


class UserCreateSchema(BaseModel):
    name: str
