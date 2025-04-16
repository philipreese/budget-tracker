from typing import Optional
from fastapi import APIRouter

from api.models import TransactionResponse, TransactionBase
from db.db import add_transaction, get_transactions
from utils.util import get_start_end_date_from_month


router = APIRouter()


@router.post("/expenses/", response_model=int, status_code=201)
async def add_expense(transaction: TransactionBase):
    """Add new expense transaction."""

    transaction.type = "expense"
    return add_transaction(transaction)


@router.get("/expenses/", response_model=list[TransactionResponse])
async def get_expenses(date: Optional[str] = None, category: Optional[str] = None):
    """Get all expenses (optionally filtered by month and category)."""

    start_date: Optional[str] = None
    end_date: Optional[str] = None
    if date:
        start_date, end_date = get_start_end_date_from_month(date)
    return get_transactions(
        start_date=start_date, end_date=end_date, category=category, type="expense"
    )
