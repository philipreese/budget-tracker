from db import *
import os
import platform


def main_menu():
    while True:
        print("\nBudget Tracker Menu:")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View Summary")
        print("4. Delete All Transactions")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            clear_terminal()
            date = get_transaction_date()
            description = get_transaction_description()
            category = get_transaction_category()
            amount = get_transaction_amount()
            add_transaction(date, description, category, amount, "income")
        elif choice == "2":
            clear_terminal()
            date = get_transaction_date()
            description = get_transaction_description()
            category = get_transaction_category()
            amount = get_transaction_amount()
            add_transaction(date, description, category, amount, "expense")
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


def clear_terminal():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")


if __name__ == "__main__":
    create_transactions_table()
    main_menu()
