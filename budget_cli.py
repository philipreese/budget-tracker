import os
import platform

from db import add_transaction, delete_all_transactions
from models import TransactionType


def main_menu() -> None:
    while True:
        print("\nBudget Tracker Menu:")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View Summary")
        print("4. Delete All Transactions")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_transaction_with_type(TransactionType.INCOME)
        elif choice == "2":
            add_transaction_with_type(TransactionType.EXPENSE)
        elif choice == "3":
            clear_terminal()
            print("Viewing summary (not yet implemented)")
        elif choice == "4":
            clear_terminal()
            delete_all_transactions()
        elif choice == "5":
            clear_terminal()
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")


def add_transaction_with_type(type: TransactionType) -> None:
    clear_terminal()
    date: str = get_transaction_date()
    description: str = get_transaction_description()
    category: str = get_transaction_category()
    amount: float = get_transaction_amount()
    add_transaction(date, description, category, amount, type)


def get_transaction_date() -> str:
    return input("Enter transaction date (YYYY-MM-DD): ")


def get_transaction_description() -> str:
    return input("Enter transaction description: ")


def get_transaction_category() -> str:
    return input("Enter transaction category (e.g., food, rent, salary): ")


def get_transaction_amount() -> float:
    while True:
        try:
            amount_str = input("Enter transaction amount: ")
            amount: float = float(amount_str)
            return amount
        except ValueError:
            print("Invalid amount. Please enter a number.")


def get_transaction_type() -> TransactionType:
    while True:
        type_choice: str = input("Enter transaction type (income/expense): ").lower()
        if type_choice == "income":
            return TransactionType.INCOME
        elif type_choice == "expense":
            return TransactionType.EXPENSE
        else:
            print("Invalid transaction type. Please enter 'income' or 'expense'.")


def clear_terminal() -> None:
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")


if __name__ == "__main__":
    from db import create_transactions_table

    create_transactions_table()
    main_menu()
