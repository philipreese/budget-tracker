"""Holds the database functions for the Budget Tracker."""

import sqlite3
from typing import Optional, Tuple, List, Any

from models import TransactionType

DATABASE_NAME: str = "budget.db"
SEED_DATA_FILE: str = "seed_data.json"


def connect() -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
    """Connects to the SQLite database."""
    conn = sqlite3.connect(DATABASE_NAME)
    return conn, conn.cursor()


def close(conn: sqlite3.Connection) -> None:
    """Closes the database connection."""
    if conn:
        conn.close()


def add_transaction(
    date: str,
    description: str,
    category: str,
    amount: float,
    transaction_type: TransactionType,
) -> int:
    """Adds a new transaction to the database."""
    conn, cursor = connect()
    try:
        cursor.execute(
            "INSERT INTO transactions (date, description, category, amount, type) VALUES (?, ?, ?, ?, ?)",
            (date, description, category, amount, str(transaction_type)),
        )
        conn.commit()
        transaction_id: Optional[int] = cursor.lastrowid
        if transaction_id is None:
            print("Error: Could not retrieve lastrowid.")
            conn.rollback()
            return -1
        return transaction_id
    except sqlite3.Error as e:
        print(f"Error adding transaction: {e}")
        conn.rollback()
        return -1
    finally:
        close(conn)


def get_all_transactions() -> List[Tuple[Any, ...]]:
    """Retrieves all transactions from the database."""
    conn, cursor = connect()
    try:
        cursor.execute("SELECT * FROM transactions")
        transactions: List[Tuple[Any, ...]] = cursor.fetchall()
        return transactions
    except sqlite3.Error as e:
        print(f"Error retrieving transactions: {e}")
        return []
    finally:
        close(conn)


def get_transactions_by_filters(
    month: Optional[str] = None,
    year: Optional[str] = None,
    category: Optional[str] = None,
) -> List[Tuple[Any, ...]]:
    """Retrieves transactions based on optional month, year, and category filters."""
    conn, cursor = connect()
    conditions: List[str] = []
    params: List[str] = []

    if month:
        conditions.append("strftime('%Y-%m', date) = ?")
        if year:
            month = f"{year}-{month}"
        params.append(month)
    if year:
        conditions.append("strftime('%Y', date) = ?")
        params.append(year)
    if category:
        conditions.append("category = ?")
        params.append(category)

    where_clause = ""
    if conditions:
        where_clause = "WHERE " + " AND ".join(conditions)

    sql = f"SELECT * FROM transactions {where_clause}"

    try:
        cursor.execute(sql, params)
        transactions: List[Tuple[Any, ...]] = cursor.fetchall()
        return transactions
    except sqlite3.Error as e:
        print(f"Error retrieving transactions by filters: {e}")
        return []
    finally:
        close(conn)


def get_transaction(transaction_id: int) -> Optional[Tuple[Any, ...]]:
    """Retrieves a single transaction by its ID."""
    conn, cursor = connect()
    cursor.execute("SELECT * FROM transactions WHERE id = ?", (transaction_id,))
    transaction: Optional[Tuple[Any, ...]] = cursor.fetchone()
    close(conn)
    return transaction


def update_transaction(
    transaction_id: int,
    date: str,
    description: str,
    category: str,
    amount: float,
    type: str,
) -> bool:
    """Updates an existing transaction in the database."""
    conn, cursor = connect()
    try:
        cursor.execute(
            """
            UPDATE transactions
            SET date = ?, description = ?, category = ?, amount = ?, type = ?
            WHERE id = ?
            """,
            (date, description, category, amount, type, transaction_id),
        )
        conn.commit()
        close(conn)
    except sqlite3.Error as e:
        print(f"Error updating transaction: {e}")
        conn.rollback()
        return False
    finally:
        if conn:
            close(conn)
        return True


def delete_all_transactions() -> bool:
    """Deletes all transactions from the database."""
    conn, cursor = connect()
    try:
        cursor.execute("DELETE FROM transactions")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='transactions'")
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error deleting transactions: {e}")
        conn.rollback()
        return False
    finally:
        close(conn)
        return True


def create_transactions_table() -> bool:
    """Creates the transaction table if it doesn't exist."""
    conn, cursor = connect()
    try:
        cursor.execute(
            """
            SELECT name FROM sqlite_master WHERE type='table' AND name='transactions';
            """
        )
        table_exists = cursor.fetchone() is not None

        if not table_exists:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    description TEXT NOT NULL,
                    category TEXT NOT NULL,
                    amount REAL NOT NULL,
                    type TEXT NOT NULL CHECK(type IN ('income', 'expense'))
                )
                """
            )
            conn.commit()
            print("Transactions table created.")
    except sqlite3.Error as e:
        print(f"Error creating transactions table: {e}")
        return False
    finally:
        close(conn)
        return True


def seed() -> bool:
    """Reads sample transactions from a JSON file and populates the database."""
    import json

    conn: sqlite3.Connection | None = None
    try:
        with open(SEED_DATA_FILE, "r", encoding="utf-8") as f:
            transactions = json.load(f)
            conn, cursor = connect()
            for transaction in transactions:
                try:
                    transaction_type = TransactionType(transaction["type"])
                    cursor.execute(
                        "INSERT INTO transactions (date, description, category, amount, type) VALUES (?, ?, ?, ?, ?)",
                        (
                            transaction["date"],
                            transaction["description"],
                            transaction["category"],
                            transaction["amount"],
                            str(transaction_type),
                        ),
                    )
                except ValueError as e:
                    print(
                        f"Warning: Invalid transaction type '{transaction["type"]}' in JSON: {e}"
                    )
            conn.commit()
            close(conn)
            print("Database seeded with sample transactions.")
    except FileNotFoundError:
        print(f"Error: {SEED_DATA_FILE} not found.")
        return False
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {SEED_DATA_FILE}.")
        return False
    except sqlite3.Error as e:
        print(f"Error seeding database: {e}")
        if conn:
            conn.rollback()
        return False
    finally:
        if conn:
            close(conn)
        return True


if __name__ == "__main__":
    create_transactions_table()
    seed()
