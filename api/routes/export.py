import csv
from io import StringIO
from typing import Optional
from fastapi import APIRouter, Response

from api.models import TransactionResponse
from cli.commands import CSV_FILENAME
from db.db import get_transactions


router = APIRouter()


@router.get("/export/csv/")
async def export_csv(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    category: Optional[str] = None,
    filename: Optional[str] = None,
    order_by: Optional[str] = None,
    order_direction: Optional[str] = None,
):
    start_date = start_date
    end_date = end_date
    category = category
    filename = filename
    order_by = order_by
    order_direction = order_direction

    transactions = get_transactions(
        start_date, end_date, category, order_by, order_direction
    )
    filename = filename or CSV_FILENAME

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(TransactionResponse.model_fields.keys())

    for transaction in transactions:
        writer.writerow(transaction.model_dump().values())

    return Response(
        content=output.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment;filename={filename}"},
    )
