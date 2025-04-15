"""Holds the CLI for the Budget Tracker."""

import argparse
from typing import Callable, Optional
from cli.models import TransactionType
from cli.commands import *


def create_parser() -> argparse.ArgumentParser:
    """Creates the argument parser"""
    parser = argparse.ArgumentParser(description="Budget Tracker CLI")
    return parser


def create_subparsers(parser: argparse.ArgumentParser):
    """Creates the subparsers for the argument parser"""
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Subparser for adding income
    add_income_parser = subparsers.add_parser(
        "add-income", help="Add an income transaction"
    )
    add_income_parser.add_argument(
        "-a", "--amount", type=float, required=True, help="Transaction amount"
    )
    add_income_parser.add_argument(
        "-d", "--date", type=str, help="Transaction date (YYYY-MM-DD), default is today"
    )
    add_income_parser.add_argument(
        "-c",
        "--category",
        type=str,
        default="Other",
        help='Transaction category, default is "Other"',
    )
    add_income_parser.add_argument(
        "-desc",
        "--description",
        type=str,
        default="Other Income",
        help='Transaction description, default is "Other Income"',
    )

    # Subparser for adding expense
    add_expense_parser = subparsers.add_parser(
        "add-expense", help="Add an expense transaction"
    )
    add_expense_parser.add_argument(
        "-a", "--amount", type=float, required=True, help="Transaction amount"
    )
    add_expense_parser.add_argument(
        "-d", "--date", type=str, help="Transaction date (YYYY-MM-DD), default is today"
    )
    add_expense_parser.add_argument(
        "-c",
        "--category",
        type=str,
        default="Other",
        help='Transaction category, default is "Other"',
    )
    add_expense_parser.add_argument(
        "-desc",
        "--description",
        type=str,
        default="Other Expense",
        help='Transaction description, default is "Other Expense"',
    )

    # Subparser for get transaction
    get_transaction_parser = subparsers.add_parser(
        "get-transaction", help="Get a single transaction by ID"
    )
    get_transaction_parser.add_argument(
        "transaction_id", type=int, help="ID of the transaction"
    )

    # Subparser for get transactions
    get_transactions_parser = subparsers.add_parser(
        "get-transactions", help="Get all transactions with optional filters"
    )
    get_transactions_parser.add_argument(
        "-s",
        "--start-date",
        type=str,
        help="Get transactions starting at this date (YYYY-MM-DD)",
    )
    get_transactions_parser.add_argument(
        "-e",
        "--end-date",
        type=str,
        help="Get transactions up to and including this date (YYYY-MM-DD)",
    )
    get_transactions_parser.add_argument(
        "-c", "--category", type=str, help="Filter transactions by category"
    )
    get_transactions_parser.add_argument(
        "-t",
        "--type",
        type=str,
        choices=[transaction_type.name.lower() for transaction_type in TransactionType],
        help="Get transactions of this type",
    )
    get_transactions_parser.add_argument(
        "-o",
        "--order-by",
        type=str,
        choices=["date", "desc", "cat", "amt", "type"],
        help="Sort transactions by column",
    )
    get_transactions_parser.add_argument(
        "-od",
        "--order-direction",
        type=str,
        choices=["asc", "desc"],
        help="Sort order (ascending (default) or descending)",
    )

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
    view_summary_parser.add_argument(
        "-e",
        "--expense",
        action="store_const",
        const=True,
        help="Show expense summary by category, default is False",
    )
    view_summary_parser.add_argument(
        "-i",
        "--income",
        action="store_const",
        const=True,
        help="Show income summary by category, default is False",
    )

    # Subparser for editing a transaction
    edit_transaction_parser = subparsers.add_parser(
        "edit-transaction", help="Edit an existing transaction"
    )
    edit_transaction_parser.add_argument(
        "transaction_id", type=int, help="ID of the transaction to edit"
    )
    edit_transaction_parser.add_argument(
        "-d", "--date", type=str, help="New transaction date (YYYY-MM-DD)"
    )
    edit_transaction_parser.add_argument(
        "-desc", "--description", type=str, help="New transaction description"
    )
    edit_transaction_parser.add_argument(
        "-c", "--category", type=str, help="New transaction category"
    )
    edit_transaction_parser.add_argument(
        "-a", "--amount", type=float, help="New transaction amount"
    )
    edit_transaction_parser.add_argument(
        "-t",
        "--type",
        type=str,
        choices=[transaction_type.name.lower() for transaction_type in TransactionType],
        help="New transaction type",
    )

    # Subparser for deleting transactions
    delete_transaction_parser = subparsers.add_parser(
        "delete-transaction",
        help="Delete transaction by ID",
    )
    delete_transaction_parser.add_argument(
        "transaction_id",
        type=int,
        help="ID of the transaction to delete. If ID is -1, deletes ALL transactions",
    )

    # Subparser for configuring
    configure_parser = subparsers.add_parser(
        "configure", help="Change configuration items"
    )
    configure_parser.add_argument(
        "-p", "--db_path", type=str, help="The path to the database file"
    )
    configure_parser.add_argument(
        "-c", "--currency-symbol", type=str, help="The currency symbol to use"
    )

    # Subparser for exporting transactions to CSV
    export_csv_subparser = subparsers.add_parser(
        "export-csv", help="Export transactions to CSV"
    )
    export_csv_subparser.add_argument(
        "-s", "--start-date", type=str, help="Start date for filtering (YYYY-MM-DD)"
    )
    export_csv_subparser.add_argument(
        "-e", "--end-date", type=str, help="End date for filtering (YYYY-MM-DD)"
    )
    export_csv_subparser.add_argument(
        "-c", "--category", type=str, help="Category to filter by"
    )
    export_csv_subparser.add_argument(
        "-f", "--filename", type=str, help="The filename of the CSV to export to"
    )
    export_csv_subparser.add_argument(
        "-o",
        "--order-by",
        type=str,
        choices=["date", "desc", "cat", "amt", "type"],
        help="Sort transactions by column",
    )
    export_csv_subparser.add_argument(
        "-od",
        "--order-direction",
        type=str,
        choices=["asc", "desc"],
        help="Sort order (ascending (default) or descending)",
    )

    # Subparser for plotting expenses by category
    plot_expenses_parser = subparsers.add_parser(
        "plot-expenses", help="Plot expenses by category"
    )
    plot_expenses_parser.add_argument(
        "-m", "--month", type=str, help="Filter expenses by month (YYYY-MM)"
    )

    return subparsers


def main():
    """Main CLI entry."""
    parser = create_parser()
    _ = create_subparsers(parser)
    args = parser.parse_args()

    command_function: Optional[Callable[[argparse.Namespace], None]] = None

    if args.command:
        command_function = {
            "add-income": add_income_command,
            "add-expense": add_expense_command,
            "view-summary": view_summary_command,
            "get-transaction": get_transaction_command,
            "get-transactions": get_transactions_command,
            "edit-transaction": edit_transaction_command,
            "delete-transaction": delete_transaction_command,
            "configure": configure_command,
            "export-csv": export_transactions_to_csv_command,
            "plot-expenses": plot_expenses_by_category_command,
        }.get(args.command)

        if command_function:
            command_function(args)
        else:
            parser.print_help()
    else:
        parser.print_help()


if __name__ == "__main__":
    from db.db import create_transactions_table

    create_transactions_table()
    main()
