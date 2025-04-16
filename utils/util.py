import calendar
import csv

from api.models import TransactionResponse


def get_start_end_date_from_month(date: str):
    year_filter, month_str = date.split("-")
    month_int = int(month_str)
    start_date = f"{date}-01"
    end_date = f"{date}-" + str(
        calendar.monthrange(int(year_filter), int(month_int))[1]
    )
    return start_date, end_date


def write_to_csv(filename: str, transactions: list[TransactionResponse]):
    try:
        with open(filename, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(TransactionResponse.model_fields.keys())
            for transaction in transactions:
                writer.writerow(transaction.model_dump().values())
            print(f"Transactions exported to {filename} successfully!")
    except Exception as e:
        print(f"Error exporting to CSV: {e}")
