import json
import sqlite3

DATABASE_NAME = "budget.db"
SEED_DATA_FILE = "seed_data.json"


def connect_db():
    """Connects to the SQLite database."""
    conn = sqlite3.connect(DATABASE_NAME)
    return conn, conn.cursor()


def close_db(conn):
    """Closes the database connection."""
    if conn:
        conn.close()


def add_transaction(date, description, category, amount, transaction_type):
    """Adds a new transaction to the database."""
    conn, cursor = connect_db()
    try:
        cursor.execute(
            "INSERT INTO transactions (date, description, category, amount, type) VALUES (?, ?, ?, ?, ?)",
            (date, description, category, amount, transaction_type),
        )
        conn.commit()
        print("Transaction added successfully!")
    except sqlite3.Error as e:
        print(f"Error adding transaction: {e}")
        conn.rollback()
    finally:
        close_db(conn)


def delete_all_transactions():
    """Deletes all transactions from the database."""
    conn, cursor = connect_db()
    try:
        cursor.execute("DELETE FROM transactions")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='transactions'")
        conn.commit()
        print("Transactions deleted successfully!")
    except sqlite3.Error as e:
        print(f"Error deleting transactions: {e}")
        conn.rollback()
    finally:
        close_db(conn)


def get_transaction_date():
    return input("Enter transaction date (YYYY-MM-DD): ")


def get_transaction_description():
    return input("Enter transaction description: ")


def get_transaction_category():
    return input("Enter transaction category (e.g., food, rent, salary): ")


def get_transaction_amount():
    while True:
        try:
            amount_str = input("Enter transaction amount: ")
            amount = float(amount_str)
            return amount
        except ValueError:
            print("Invalid amount. Please enter a number.")


def get_transaction_type():
    while True:
        type_choice = input("Enter transaction type (income/expense): ").lower()
        if type_choice in ["income", "expense"]:
            return type_choice
        else:
            print("Invalid transaction type. Please enter 'income' or 'expense'.")


def create_transactions_table():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    CREATE_TABLE_QUERY = """
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        description TEXT NOT NULL,
        category TEXT NOT NULL,
        amount REAL NOT NULL,
        type TEXT NOT NULL CHECK(type IN ('income', 'expense'))
    );
    """

    cursor.execute(CREATE_TABLE_QUERY)
    conn.commit()
    conn.close()
    print(
        f"Database '{DATABASE_NAME}' created and 'transactions' table set up (if it didn't exist)."
    )


def seed_database():
    """Reads sample transactions from a JSON file and populates the database."""
    try:
        with open(SEED_DATA_FILE, "r") as f:
            transactions = json.load(f)
            conn, cursor = connect_db()
            for transaction in transactions:
                cursor.execute(
                    "INSERT INTO transactions (date, description, category, amount, type) VALUES (?, ?, ?, ?, ?)",
                    (
                        transaction["date"],
                        transaction["description"],
                        transaction["category"],
                        transaction["amount"],
                        transaction["type"],
                    ),
                )
            conn.commit()
            close_db(conn)
            print("Database seeded with sample transactions.")
    except FileNotFoundError:
        print(f"Error: {SEED_DATA_FILE} not found.")
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {SEED_DATA_FILE}.")
    except sqlite3.Error as e:
        print(f"Error seeding database: {e}")
        if "conn" in locals():
            conn.rollback()
            close_db(conn)


if __name__ == "__main__":
    create_transactions_table()
    seed_database()
