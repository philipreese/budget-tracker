import sqlite3

DATABASE_NAME = "budget.db"


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


if __name__ == "__main__":
    create_transactions_table()
