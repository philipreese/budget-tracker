import argparse
import calendar
from datetime import date
from typing import Any, List, Tuple
from db import (
    add_transaction,
    delete_all_transactions,
    delete_transaction,
    get_transaction,
    get_transactions_by_filters,
    update_transaction,
)
from models import TransactionType


def add_income_command(args: argparse.Namespace) -> None:
    add_transaction_command(args, TransactionType.INCOME)


def add_expense_command(args: argparse.Namespace) -> None:
    add_transaction_command(args, TransactionType.EXPENSE)


def add_transaction_command(
    args: argparse.Namespace, transaction_type: TransactionType
) -> None:
    """Adds a transaction (income or expense) based on arguments."""
    transaction_date = args.date if args.date else str(date.today())
    amount = args.amount
    category = args.category if args.category else "other"
    description = (
        args.description if args.description else f"other {transaction_type.value}"
    )

    transaction_id = add_transaction(
        transaction_date, description, category, amount, transaction_type
    )
    if transaction_id > 0:
        print(f"{transaction_type.value.capitalize()} added successfully.")
        get_transaction_command(argparse.Namespace(transaction_id=transaction_id))


def calculate_summary(
    transactions: List[Tuple[Any, ...]],
) -> Tuple[float, float, float]:
    """Calculates the summary (total income, expenses, balance)."""
    total_income: float = 0.0
    total_expenses: float = 0.0
    for transaction in transactions:
        amount: float = transaction[4]
        transaction_type_str: str = transaction[5]
        if transaction_type_str == str(TransactionType.INCOME):
            total_income += amount
        elif transaction_type_str == str(TransactionType.EXPENSE):
            total_expenses += amount
    net_balance: float = total_income - total_expenses
    return total_income, total_expenses, net_balance


def get_month_name(month_number: str) -> str:
    """Converts a month number (MM) to its name."""
    try:
        month_int = int(month_number)
        if 1 <= month_int <= 12:
            return calendar.month_name[month_int]
        return ""
    except ValueError:
        return ""


def view_summary_command(args: argparse.Namespace) -> None:
    """Command to view the transaction summary."""
    month_filter: str = args.month
    year_filter: str = args.year
    category_filter: str = args.category
    transactions: List[Tuple[Any, ...]] = []
    filter_description = "Overall"
    query_month = None
    query_year = None

    if month_filter:
        if len(month_filter) == 7 and month_filter[4] == "-":
            query_year, query_month = month_filter.split("-")
            month_name = get_month_name(query_month)
            filter_description = (
                f"for {month_name} {query_year}"
                if month_name and query_year
                else f"for {month_filter}"
            )
        elif (
            0 < len(month_filter) <= 2
            and month_filter.isdigit()
            and 1 <= int(month_filter) <= 12
        ):
            month_filter = (
                month_filter if len(month_filter) == 2 else f"0{month_filter}"
            )
            query_month = month_filter
            month_name = get_month_name(query_month)
            filter_description = f"for {month_name}"
            if year_filter:
                query_year = year_filter
                filter_description = f"for {month_name} {year_filter}"
            else:
                print("Must specify year along with month")
                return
        else:
            print("Invalid month format. Please use MM or YYYY-MM.")
            return
    elif year_filter:
        if len(year_filter) == 4 and year_filter.isdigit():
            query_year = year_filter
            filter_description = f"for {year_filter}"
        else:
            print("Invalid year format. Please use YYYY.")
            return

    if category_filter:
        filter_description = (
            f"for category '{category_filter}'"
            if not month_filter and not year_filter
            else f"{filter_description}, category '{category_filter}'"
        )

    transactions = get_transactions_by_filters(
        month=month_filter, year=year_filter, category=category_filter
    )

    print(f"\n--- Transaction Summary ({filter_description}) ---")

    if transactions:
        total_income, total_expenses, net_balance = calculate_summary(transactions)
        print(f"Total Income: ${total_income:.2f}")
        print(f"Total Expenses: ${total_expenses:.2f}")
        print(f"Net Balance: ${net_balance:.2f}")
    else:
        print(
            "No transactions found for the specified filters."
            if month_filter or year_filter or category_filter
            else "No transactions found."
        )


def edit_transaction_command(args: argparse.Namespace) -> None:
    """Command for editing an existing transaction."""
    transaction_id = args.transaction_id

    if (
        args.date is None
        and args.description is None
        and args.category is None
        and args.amount is None
        and args.type is None
    ):
        print("Must include at least one option for editing a transaction")
        return

    # Retrieve the transaction from the database
    transaction = get_transaction(transaction_id)
    if not transaction:
        print(f"Transaction with ID {transaction_id} not found.")
        return

    # Collect updates from flags
    new_date = args.date or transaction[1]
    new_description = args.description or transaction[2]
    new_category = args.category or transaction[3]
    new_amount = args.amount or transaction[4]
    new_type = args.type or transaction[5]

    # Update the transaction in the database
    update_transaction(
        transaction_id, new_date, new_description, new_category, new_amount, new_type
    )

    print("Transaction updated successfully!")
    get_transaction_command(args)


def get_transaction_command(args: argparse.Namespace) -> None:
    """Command to get a transaction by ID."""
    transaction = get_transaction(args.transaction_id)
    if not transaction:
        print("No transaction exists with that ID.")
        return
    print(f"\n--- Transaction ID {transaction[0]} ---")
    print(f"Date: {transaction[1]}")
    print(f"Description: {transaction[2]}")
    print(f"Category: {transaction[3]}")
    print(f"Amount: ${transaction[4]:.2f}")
    print(f"Type: {transaction[5]}")


def delete_transaction_command(args: argparse.Namespace) -> None:
    """Command to delete a transaction by ID."""

    transaction_id = args.transaction_id
    if transaction_id == -1:
        if delete_all_transactions():
            print("All transactions deleted successfully")
            return

    if delete_transaction(transaction_id):
        print(f"Transaction with ID {transaction_id} deleted successfully!")
    else:
        print(
            f"Transaction with ID {transaction_id} not found or could not be deleted."
        )
