from typing import Optional
from fastapi import APIRouter

from api.models import TransactionBase, TransactionResponse
from db.db import add_transaction, get_transactions
from utils.util import get_start_end_date_from_month


router = APIRouter()


@router.post("/income/", response_model=int, status_code=201)
async def add_income(transaction: TransactionBase):
    """Add new income transaction."""

    transaction.type = "income"
    return add_transaction(transaction)


@router.get("/income/", response_model=list[TransactionResponse])
async def get_income(date: Optional[str] = None):
    """Get all income (optionally filtered by month)."""

    start_date: Optional[str] = None
    end_date: Optional[str] = None
    if date:
        start_date, end_date = get_start_end_date_from_month(date)
    return get_transactions(start_date=start_date, end_date=end_date, type="income")
