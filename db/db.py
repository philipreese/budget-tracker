"""Holds the database functions for the Budget Tracker."""

import json
import os
import sqlite3
from typing import Optional, Tuple, List, Any
from api.models import TransactionBase, TransactionResponse
from cli.models import TransactionType

CONFIG_FILE = "config.json"
DEFAULT_DATABASE_NAME: str = "budget.db"
DEFAULT_CURRENCY: str = "$"

SEED_DATA_FILE: str = "seed_data.json"
SELECT_TRANSACTIONS_TABLE = """
    SELECT name FROM sqlite_master WHERE type='table' AND name='transactions';
    """
CREATE_TRANSACTIONS_TABLE = """
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        description TEXT NOT NULL,
        category TEXT NOT NULL,
        amount REAL NOT NULL,
        type TEXT NOT NULL CHECK(type IN ('income', 'expense'))
    )
    """
INSERT_TRANSACTION = """
    INSERT INTO transactions (date, description, category, amount, type)
    VALUES (?, ?, ?, ?, ?)
    """
GET_TRANSACTION = "SELECT * FROM transactions WHERE id = ?"
GET_TRANSACTIONS = "SELECT * FROM transactions"
DELETE_TRANSACTION = "DELETE FROM transactions WHERE id = ?"


def get_config() -> dict[str, str]:
    """Reads the configuration from a JSON file or returns defaults."""
    config: dict[str, str] = {}
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                config = json.load(f)
        except json.JSONDecodeError:
            print(f"Warning: Invalid JSON in {CONFIG_FILE}. Using defaults.")
    return {
        "db_path": config.get("db_path", DEFAULT_DATABASE_NAME),
        "currency_symbol": config.get("currency_symbol", DEFAULT_CURRENCY),
    }


def get_database_path() -> str:
    """Gets the database path from the configuration."""
    config = get_config()
    return config.get("db_path", DEFAULT_DATABASE_NAME)


def connect() -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
    """Connects to the SQLite database."""
    database_path = get_database_path()
    conn = sqlite3.connect(database_path)
    return conn, conn.cursor()


def close(conn: sqlite3.Connection) -> None:
    """Closes the database connection."""
    if conn:
        conn.close()


def create_transactions_table() -> bool:
    """
    Creates the transaction table if it doesn't exist. Returns True if the
    transaction table exists or is successfully created; False otherwise.
    """
    conn, cursor = connect()
    try:
        cursor.execute(SELECT_TRANSACTIONS_TABLE)
        table_exists = cursor.fetchone() is not None

        if not table_exists:
            cursor.execute(CREATE_TRANSACTIONS_TABLE)
            conn.commit()
            print("Transactions table created.")
        return True
    except sqlite3.Error as e:
        print(f"Error creating transactions table: {e}")
        return False
    finally:
        close(conn)


def add_transaction(transaction: TransactionBase) -> int:
    """
    Adds a new transaction to the database. Returns the ID if the add
    was successful; -1 otherwise.
    """
    conn, cursor = connect()
    try:
        cursor.execute(
            INSERT_TRANSACTION,
            (list(transaction.model_dump().values())),
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


def get_transaction(transaction_id: int) -> Optional[Tuple[Any, ...]]:
    """Retrieves a single transaction by its ID."""
    conn, cursor = connect()
    cursor.execute(GET_TRANSACTION, (transaction_id,))
    transaction: Optional[Tuple[Any, ...]] = cursor.fetchone()
    close(conn)
    return transaction


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


def get_transactions(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    category: Optional[str] = None,
    order_by: Optional[str] = None,
    order_direction: Optional[str] = None,
    type: Optional[str] = None,
) -> List[TransactionResponse]:
    """Retrieves transactions from the database with optional filtering."""

    conn, cursor = connect()
    query = GET_TRANSACTIONS
    conditions: List[str] = []
    params: List[str] = []

    if start_date:
        conditions.append("date >= ?")
        params.append(start_date)
    if end_date:
        conditions.append("date <= ?")
        params.append(end_date)
    if category:
        conditions.append("category = ?")
        params.append(category)
    if type:
        conditions.append("type = ?")
        params.append(type)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    if order_by:
        match order_by:
            case "date":
                pass
            case "desc":
                order_by = "description"
            case "cat":
                order_by = "category"
            case "amt":
                order_by = "amount"
            case "type":
                pass
            case _:
                raise ValueError(f"Invalid order_by column: {order_by}")
        query += f" ORDER BY {order_by}"

    if order_direction:
        if order_direction.upper() not in ("ASC", "DESC"):
            raise ValueError(f"Invalid order_direction: {order_direction}")
        query += f" {order_direction.upper()}"

    try:
        cursor.execute(query, params)
        transactions: List[Tuple[Any, ...]] = cursor.fetchall()

        result: list[TransactionResponse] = []
        for transaction in transactions:
            transaction_dict = {
                "id": transaction[0],
                "date": transaction[1],
                "description": transaction[2],
                "category": transaction[3],
                "amount": transaction[4],
                "type": transaction[5],
            }
            result.append(TransactionResponse(**transaction_dict))
        return result
    except sqlite3.Error as e:
        print(f"Error retrieving transactions: {e}")
        return []
    finally:
        close(conn)


def update_transaction(transaction_id: int, transaction: TransactionBase) -> bool:
    """Updates an existing transaction in the database."""
    conn, cursor = connect()
    try:
        cursor.execute(
            """
            UPDATE transactions
            SET date = ?, description = ?, category = ?, amount = ?, type = ?
            WHERE id = ?
            """,
            (*list(transaction.model_dump().values()), transaction_id),
        )
        conn.commit()
        close(conn)
        return True
    except sqlite3.Error as e:
        print(f"Error updating transaction: {e}")
        conn.rollback()
        return False
    finally:
        if conn:
            close(conn)


def delete_transaction(transaction_id: int) -> bool:
    """
    Deletes a transaction by its ID.
    Returns True if successful, False otherwise.
    """
    conn, cursor = connect()
    try:
        cursor.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
        conn.commit()
        return cursor.rowcount > 0  # rowcount > 0 indicates a row was deleted
    except sqlite3.Error as e:
        print(f"Error deleting transaction: {e}")
        conn.rollback()
        return False
    finally:
        close(conn)


def delete_all_transactions() -> bool:
    """Deletes all transactions from the database."""
    conn, cursor = connect()
    try:
        cursor.execute("DELETE FROM transactions")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='transactions'")
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error deleting transactions: {e}")
        conn.rollback()
        return False
    finally:
        close(conn)


def seed() -> bool:
    """Reads sample transactions from a JSON file and populates the database."""

    conn: sqlite3.Connection | None = None
    try:
        with open(SEED_DATA_FILE, "r", encoding="utf-8") as f:
            transactions = json.load(f)
            conn, cursor = connect()
            for transaction in transactions:
                try:
                    transaction_type = TransactionType(transaction["type"])
                    cursor.execute(
                        """
                        INSERT INTO transactions (date, description, category, amount, type)
                        VALUES (?, ?, ?, ?, ?)
                        """,
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
        print(f"Database seeded with {len(transactions)} sample transactions.")
        return True
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


if __name__ == "__main__":
    create_transactions_table()
    seed()
