from typing import Optional
from fastapi import APIRouter
from api.models import SummaryResponse
from db import db


router = APIRouter()


@router.get("/summary/", response_model=SummaryResponse)
async def get_summary(date: Optional[str] = None):
    """Get the total income, total expenses, and net balance (optionally filtered by month)."""

    summary_data = db.get_summary(date)
    return SummaryResponse(**summary_data)
