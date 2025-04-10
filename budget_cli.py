"""Holds the CLI for the Budget Tracker."""

import argparse
import calendar
from datetime import date
from typing import Any, Callable, List, Tuple
from db import add_transaction, delete_all_transactions, get_transactions_by_filters
from models import TransactionType


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

    add_transaction(transaction_date, description, category, amount, transaction_type)
    print(f"{transaction_type.value.capitalize()} added successfully.")


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


def delete_transactions_command() -> None:
    """Command to delete all transactions."""
    delete_all_transactions()


def main():
    """Main CLI entry."""
    parser = argparse.ArgumentParser(description="Budget Tracker CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Subparser for adding income
    add_income_parser = subparsers.add_parser(
        "add-income", help="Add an income transaction"
    )
    add_income_parser.add_argument(
        "-d", "--date", type=str, help="Transaction date (YYYY-MM-DD), default is today"
    )
    add_income_parser.add_argument(
        "-a", "--amount", type=float, required=True, help="Transaction amount"
    )
    add_income_parser.add_argument(
        "-c",
        "--category",
        type=str,
        default="other",
        help='Transaction category, default is "other"',
    )
    add_income_parser.add_argument(
        "-desc",
        "--description",
        type=str,
        default="other income",
        help="Transaction description",
    )
    income_lambda: Callable[[argparse.Namespace], None] = (
        lambda args: add_transaction_command(args, TransactionType.INCOME)
    )
    add_income_parser.set_defaults(func=income_lambda)

    # Subparser for adding expense
    add_expense_parser = subparsers.add_parser(
        "add-expense", help="Add an expense transaction"
    )
    add_expense_parser.add_argument(
        "-d", "--date", type=str, help="Transaction date (YYYY-MM-DD), default is today"
    )
    add_expense_parser.add_argument(
        "-a", "--amount", type=float, required=True, help="Transaction amount"
    )
    add_expense_parser.add_argument(
        "-c", "--category", type=str, default="other", help="Transaction category"
    )
    add_expense_parser.add_argument(
        "-desc",
        "--description",
        type=str,
        default="other expense",
        help="Transaction description",
    )
    expense_lambda: Callable[[argparse.Namespace], None] = (
        lambda args: add_transaction_command(args, TransactionType.EXPENSE)
    )
    add_expense_parser.set_defaults(func=expense_lambda)

    # Subparser for deleting transactions
    delete_transactions_parser = subparsers.add_parser(
        "delete-transactions", help="Delete all transactions"
    )
    delete_lambda: Callable[[argparse.Namespace], None] = (
        lambda args: delete_transactions_command()
    )
    delete_transactions_parser.set_defaults(func=delete_lambda)

    # Subparser for viewing summary
    view_summary_parser = subparsers.add_parser(
        "view-summary", help="View transaction summary"
    )
    view_summary_parser.add_argument(
        "-m",
        "--month",
        type=str,
        help="Filter summary by month (YYYY-MM or MM if also using --year)",
    )
    view_summary_parser.add_argument(
        "-y", "--year", type=str, help="Filter summary by year (YYYY)"
    )
    view_summary_parser.add_argument(
        "-c", "--category", type=str, help="Filter summary by category"
    )

    summary_lambda: Callable[[argparse.Namespace], None] = (
        lambda args: view_summary_command(args)
    )
    view_summary_parser.set_defaults(func=summary_lambda)

    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    from db import create_transactions_table

    create_transactions_table()
    main()
