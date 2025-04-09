"""Holds the CLI for the Budget Tracker."""

import argparse
from datetime import date
from typing import Any, Callable, List, Tuple
from db import add_transaction, get_all_transactions, delete_all_transactions
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


def view_summary_command() -> None:
    """Command to view the transaction summary."""
    transactions: List[Tuple[Any, ...]] = get_all_transactions()
    if transactions:
        total_income, total_expenses, net_balance = calculate_summary(transactions)
        print("\n--- Transaction Summary ---")
        print(f"Total Income: ${total_income:.2f}")
        print(f"Total Expenses: ${total_expenses:.2f}")
        print(f"Net Balance: ${net_balance:.2f}")
    else:
        print("No transactions found.")


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
    summary_lambda: Callable[[argparse.Namespace], None] = (
        lambda args: view_summary_command()
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
