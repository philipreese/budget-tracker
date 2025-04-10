"""Holds the CLI for the Budget Tracker."""

import argparse
from typing import Callable, Optional
from models import TransactionType

from commands_cli import (
    add_expense_command,
    add_income_command,
    add_transaction_command,
    delete_transactions_command,
    edit_transaction_command,
    get_transaction_command,
    view_summary_command,
)
from models import TransactionType


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Budget Tracker CLI")
    return parser


def create_subparsers(parser: argparse.ArgumentParser):
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
        default="other",
        help='Transaction category, default is "other"',
    )
    add_income_parser.add_argument(
        "-desc",
        "--description",
        type=str,
        default="other income",
        help='Transaction description, default is "other income"',
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
        "-a", "--amount", type=float, required=True, help="Transaction amount"
    )
    add_expense_parser.add_argument(
        "-d", "--date", type=str, help="Transaction date (YYYY-MM-DD), default is today"
    )
    add_expense_parser.add_argument(
        "-c",
        "--category",
        type=str,
        default="other",
        help='Transaction category, default is "other"',
    )
    add_expense_parser.add_argument(
        "-desc",
        "--description",
        type=str,
        default="other expense",
        help='Transaction description, default is "other expense"',
    )
    expense_lambda: Callable[[argparse.Namespace], None] = (
        lambda args: add_transaction_command(args, TransactionType.EXPENSE)
    )
    add_expense_parser.set_defaults(func=expense_lambda)

    get_transaction_parser = subparsers.add_parser(
        "get-transaction", help="Get a single transaction by ID"
    )
    get_transaction_parser.add_argument(
        "transaction_id", type=int, help="ID of the transaction"
    )
    get_transaction_parser.set_defaults(func=get_transaction_command)

    # Subparser for deleting transactions
    delete_transactions_parser = subparsers.add_parser(
        "delete-transactions", help="Delete all transactions"
    )
    delete_lambda: Callable[[argparse.Namespace], None] = (
        lambda args: delete_transactions_command(args)
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
    edit_transaction_parser.set_defaults(func=edit_transaction_command)

    return subparsers


def main():
    """Main CLI entry."""
    parser = create_parser()
    _ = create_subparsers(parser)
    args = parser.parse_args()

    command_function: Optional[Callable[[argparse.Namespace], None]] = None

    if args.command:
        if args.command == "add-income":
            command_function = add_income_command
        elif args.command == "add-expense":
            command_function = add_expense_command
        elif args.command == "view-summary":
            command_function = view_summary_command
        elif args.command == "edit-transaction":
            command_function = edit_transaction_command
        elif args.command == "delete-transactions":
            command_function = delete_transactions_command

        if command_function:
            command_function(args)
        else:
            parser.print_help()
    else:
        parser.print_help()


if __name__ == "__main__":
    from db import create_transactions_table

    create_transactions_table()
    main()
