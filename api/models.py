from datetime import date


from pydantic import BaseModel


class TransactionBase(BaseModel):
    date: date
    description: str
    category: str
    amount: float
    type: str = "income"


class TransactionResponse(TransactionBase):
    id: int


class SummaryResponse(BaseModel):
    total_income: float
    total_expenses: float
    net_balance: float
