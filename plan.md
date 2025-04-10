# Plan
## Phase 1: Core Functionality (Command-Line Interface)

- Goal: Implement the basic ability to add transactions and view a simple summary in the terminal.
- Tasks:
    1. Database Setup (SQLite):
       - Define the database schema (e.g., `transactions` table with columns: `id`, `date`, `description`, `category`, `amount`, `type` ('income' or 'expense')).
       - Write Python code using the `sqlite3` library to create the database and the `transactions` table if it doesn't exist.
    2. Adding Transactions:
        - Create functions to prompt the user for transaction details (date, description, category, amount, type).
        - Write a function to insert this data into the `transactions` table.
    3. Viewing Summary:
        - Write functions to:
            - Retrieve all income transactions from the database and calculate the total.
            - Retrieve all expense transactions from the database and calculate the total.
            - Calculate the net balance (total income - total expenses).
        - Display this summary in the terminal.
    4. Basic User Interface (CLI):
        - Create a simple command-line menu that allows the user to choose options like "Add Income," "Add Expense," "View Summary," and "Exit."
  
## Phase 2: Persistence and Basic Filtering (CLI)

- Goal: Ensure data is saved persistently and introduce basic filtering.
- Tasks:
    1. Refactor Database Interactions:
        - Organize database interactions into reusable functions (e.g., `add_transaction`, `get_all_transactions`).
    2. Filtering by Month:
        - Implement a function that prompts the user for a month (e.g., YYYY-MM).
        - Write a database query to retrieve transactions within that specific month.
        - Update the "View Summary" option to allow filtering by month.
    3. Filtering by Category:
        - Implement a function that prompts the user for a category.
        - Write a database query to retrieve transactions belonging to that category.
        - Allow filtering the summary by category as well.
  
## Phase 3: More Advanced Features (CLI):
    - Allowing users to edit or delete existing transactions.
    - Implementing more sophisticated reporting (e.g., expenses by category over time).
    - Potentially adding configuration options.

## Phase 4: Exporting and Visualization (CLI)

- Goal: Add the ability to export data and visualize spending.
- Tasks:
    1. Export to CSV:
        - Create a function that retrieves all transactions (or filtered transactions).
        - Use the `csv` module to write this data to a CSV file.
        - Prompt the user for a filename.
    2. Bar Graph of Spending:
        - Introduce the `matplotlib` library.
        - Create a function that:
            - Retrieves expense transactions (optionally filtered by month).
            - Groups expenses by category and calculates the total spending per category.
            - Generates a bar graph displaying the spending per category.
            -Display the graph to the user (or save it as an image).

## Phase 5: REST API with FastAPI

- Goal: Expose the budget tracker functionality through a REST API.
- Tasks:
    1. Install FastAPI and Uvicorn:

        `pip install fastapi uvicorn`

    2. Create API Endpoints:
        - `/income/`:
            - `POST`: Add new income.
            - `GET`: Get all income (with optional query parameters for filtering by month).
        - `/expenses/`:
          - `POST`: Add new expense.
          - `GET`: Get all expenses (with optional query parameters for filtering by month and category).
        - `/summary/`:
          - `GET`: Get the total income, total expenses, and net balance (with optional query parameters for filtering by month).
        - `/export/csv/`:
          - `GET`: Export transactions to a CSV file (consider how to handle filtering here, possibly through query parameters).
    3. Pydantic Models:
        - Define Pydantic models for request and response bodies (e.g., `TransactionCreate`, `TransactionResponse`, `SummaryResponse`).
    4. Database Integration in FastAPI:
        - Ensure your FastAPI application can interact with your SQLite database. You might need to create database utility functions that your API routes can call.
    5. Run the FastAPI Application:

        `uvicorn main:app --reload`

        (Assuming your FastAPI application is in a file named main.py and the app instance is named app).

## Phase 6: Enhancements and Refinements (Optional)

- Goal: Improve the application based on your learning and potential user feedback.
- Possible Tasks:
    - More Advanced Filtering: Allow filtering by date ranges, multiple categories, etc.
    - User Interface (GUI): Consider building a simple graphical user interface using libraries like Tkinter or PyQt (this would be a significant expansion).
    - Data Validation: Implement more robust input validation.
    - Error Handling: Add more comprehensive error handling.
    - Configuration: Allow users to configure database location, etc.
    - Testing: Write unit and integration tests.
    - Deployment: Learn how to deploy your FastAPI application.