"""Holds the commands used for the CLI."""

import argparse
import calendar
from datetime import date
import json
from typing import Any, List, Optional, Tuple
from api.models import TransactionBase
from db.db import *
from cli.models import TransactionType
import matplotlib

from utils.util import write_to_csv

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

CSV_FILENAME = "transactions.csv"


def add_income_command(args: argparse.Namespace) -> None:
    """Calls the add_transaction_command with income type."""
    add_transaction_command(args, TransactionType.INCOME)


def add_expense_command(args: argparse.Namespace) -> None:
    """Calls the add_transaction_command with expense type."""
    add_transaction_command(args, TransactionType.EXPENSE)


def add_transaction_command(
    args: argparse.Namespace, transaction_type: TransactionType
) -> None:
    """Adds a transaction (income or expense) based on arguments."""
    transaction: TransactionBase = TransactionBase(
        date=args.date if args.date else date.today(),
        description=args.description,
        category=args.category,
        amount=args.amount,
        type=str(transaction_type),
    )

    transaction_id = add_transaction(transaction)
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


def get_transaction_command(args: argparse.Namespace) -> None:
    """Command to get a transaction by ID."""

    config = get_config()
    transaction = get_transaction(args.transaction_id)
    if not transaction:
        print("No transaction exists with that ID.")
        return
    print(f"\n--- Transaction ID {transaction[0]} ---")
    print(f"Date: {transaction[1]}")
    print(f"Description: {transaction[2]}")
    print(f"Category: {transaction[3]}")
    print(f"Amount: {config["currency_symbol"]}{transaction[4]:.2f}")
    print(f"Type: {str(transaction[5]).capitalize()}")


def get_transactions_command(args: argparse.Namespace) -> None:
    """Gets transactions by category, optionally within a date range."""

    config = get_config()
    start_date: Optional[str] = args.start_date
    end_date: Optional[str] = args.end_date
    category: Optional[str] = args.category
    order_by: Optional[str] = args.order_by
    order_direction: Optional[str] = args.order_direction
    type: Optional[str] = args.type

    transactions = get_transactions(
        start_date, end_date, category, order_by, order_direction, type
    )
    print(f"\n{len(transactions)} transactions found!")
    print("\n--- Transaction Details ---")

    if transactions:
        # Calculate max lengths for formatting
        max_date_len = max(len(str(t.date)) for t in transactions)
        max_desc_len = max(len(t.description) for t in transactions)
        max_cat_len = max(max(len(t.category) for t in transactions), 8)
        max_am_len = max(len(format(t.amount, ",.2f")) + 1 for t in transactions)

        header = (
            f" {'Date':<{max_date_len}} | "
            f"{'Description':<{max_desc_len}} | "
            f"{'Category':<{max_cat_len}} | "
            f"{'Amount':>{max_am_len+1}} | "
            f"{'Type':<6} "
        )
        print("-" * len(header))
        print(header)
        print("-" * len(header))

        for t in transactions:
            print(
                (
                    f" {str(t.date):<{max_date_len}} | "
                    f"{t.description:<{max_desc_len}} | "
                    f"{t.category:<{max_cat_len}} | "
                    f"{config["currency_symbol"]} {t.amount:>{max_am_len - 1},.2f} | "
                    f"{str(t.type).capitalize()}"
                )
            )
    else:
        print("No transactions to display.")


def view_summary_command(args: argparse.Namespace) -> None:
    """Command to view the transaction summary."""

    config = get_config()
    month_filter: Optional[str] = args.month
    year_filter: Optional[str] = args.year
    category_filter: Optional[str] = args.category

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
        currency_symbol = config["currency_symbol"]
        total_income, total_expenses, net_balance = calculate_summary(transactions)
        print(f"Total Income: {currency_symbol}{total_income:,.2f}")
        print(f"Total Expenses: {currency_symbol}{total_expenses:,.2f}")
        print(f"Net Balance: {currency_symbol}{net_balance:,.2f}")

        if args.expense:
            _detail_print(transactions, TransactionType.EXPENSE, currency_symbol)
        if args.income:
            _detail_print(transactions, TransactionType.INCOME, currency_symbol)
    else:
        print(
            "No transactions found for the specified filters."
            if month_filter or year_filter or category_filter
            else "No transactions found."
        )


def _detail_print(
    transactions: List[Tuple[Any, ...]],
    transaction_type: TransactionType,
    currency_symbol: str,
):
    type_str = transaction_type.name.lower()

    print(f"\n--- {type_str.capitalize()} by Category ---")
    items = [t for t in transactions if t[5] == type_str]
    items_by_category: dict[str, float] = {}
    for item in items:
        cat = item[3]
        amt = item[4]
        items_by_category[cat] = items_by_category.get(cat, 0) + amt

    max_cat_len = max(len(c) for c in items_by_category) if items_by_category else 0
    print("-" * (max_cat_len + 15))
    for cat, amt in sorted(items_by_category.items()):
        print(f" {cat:<{max_cat_len}}  {currency_symbol} {amt:>{10},.2f} ")


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
    transaction_create: TransactionBase = TransactionBase(
        date=args.date or transaction[1],
        description=args.description or transaction[2],
        category=args.category or transaction[3],
        amount=args.amount or transaction[4],
        type=args.type or transaction[5],
    )
    # Update the transaction in the database
    update_transaction(transaction_id, transaction_create)

    print("Transaction updated successfully!")
    get_transaction_command(args)


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


def configure_command(args: argparse.Namespace) -> None:
    """Command to allow the user to configure application settings."""

    config = get_config()
    new_db_path = args.db_path or config["db_path"]
    currency_symbol = args.currency_symbol or config["currency_symbol"]

    config["db_path"] = new_db_path
    config["currency_symbol"] = currency_symbol

    with open(CONFIG_FILE, "w", encoding="utf-8") as config_file:
        json.dump(config, config_file, indent=4)

    print("Configuration saved successfully!")


def export_transactions_to_csv_command(args: argparse.Namespace) -> None:
    """Exports transactions to a CSV file."""

    start_date: Optional[str] = args.start_date
    end_date: Optional[str] = args.end_date
    category: Optional[str] = args.category
    filename: Optional[str] = args.filename
    order_by: Optional[str] = args.order_by
    order_direction: Optional[str] = args.order_direction

    transactions = get_transactions(
        start_date, end_date, category, order_by, order_direction
    )
    filename = filename or CSV_FILENAME

    write_to_csv(filename, transactions)


def plot_expenses_by_category_command(args: argparse.Namespace) -> None:
    """Plots a bar graph of expenses by category."""

    month_filter: Optional[str] = args.month
    year_filter: Optional[str] = None
    month_str: Optional[str] = None
    month_int: Optional[int] = None

    if month_filter:
        try:
            year_filter, month_str = month_filter.split("-")
            month_int = int(month_str)
            if not (1 <= month_int <= 12 and len(year_filter) == 4):
                raise ValueError
        except ValueError:
            print(f"Error: Invalit month format. Please use YYYY-MM")
            return

    start_date: Optional[str] = (
        f"{year_filter}-{month_str}-01" if month_filter else None
    )
    end_date: Optional[str] = None
    if year_filter and month_int:
        end_date = (
            f"{year_filter}-{month_str}-"
            + str(calendar.monthrange(int(year_filter), int(month_int))[1])
            if month_filter
            else None
        )

    transactions = get_transactions(start_date, end_date, order_by="date")
    expenses_by_category: dict[str, float] = {}
    for t in transactions:
        if t.type == "expense":
            category = t.category
            amount = t.amount
            expenses_by_category[category] = (
                expenses_by_category.get(category, 0) + amount
            )

    if not expenses_by_category:
        print("No expenses found for the specified period.")
        return

    categories = list(expenses_by_category.keys())
    spending = list(expenses_by_category.values())

    plt.figure(figsize=(10, 6))  # type: ignore
    plt.bar(categories, spending, color="skyblue")  # type: ignore
    plt.xlabel("Expense Category")  # type: ignore
    plt.ylabel("Total Spending")  # type: ignore
    plt.title(  # type: ignore
        f"Expenses by Category {'for ' + month_filter if month_filter else 'Overall'}"
    )
    plt.xticks(rotation=45, ha="right")  # type: ignore
    plt.tight_layout()
    plt.show()  # type: ignore
