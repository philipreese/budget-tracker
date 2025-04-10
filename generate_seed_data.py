from collections import defaultdict
import json
import random
from datetime import datetime, date, timedelta
from typing import Dict, List, Union


def generate_seed_data(
    start_date_str: str, end_date_str: str, num_rows: int, categories: List[str]
) -> List[Dict[str, Union[str, float]]]:
    """
    Generates seed data for budget tracker transactions.

    Args:
        start_date_str: Start date for the range (YYYY-MM-DD).
        end_date_str: End date for the range (YYYY-MM-DD).
        num_rows: Number of transaction rows to generate.
        categories: List of possible transaction categories.

    Returns:
        A list of transaction dictionaries.
    """
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
    time_difference = end_date - start_date
    transactions: List[Dict[str, Union[str, float]]] = []
    salary_counts_per_month: Dict[str, int] = defaultdict(int)
    salary_category = "Salary"

    income_keywords = ["salary", "deposit", "freelance", "investment", "bonus", "gift"]
    expense_keywords = [
        "grocery",
        "rent",
        "bill",
        "shopping",
        "food",
        "entertainment",
        "transport",
        "payment",
        "subscription",
    ]

    # Generate forced salary transactions
    current_date = start_date
    while current_date <= end_date:
        year_month = current_date.strftime("%Y-%m")
        # Ensure 2 salary transactions per month
        for _ in range(2 - salary_counts_per_month[year_month]):
            first_day_of_next_month: date
            if current_date.month == 12:
                first_day_of_next_month = current_date.replace(
                    day=1, month=1, year=current_date.year + 1
                )
            else:
                first_day_of_next_month = current_date.replace(
                    day=1, month=current_date.month + 1, year=current_date.year
                )

            last_day_of_current_month = first_day_of_next_month - timedelta(days=1)
            day_of_month = random.randint(1, last_day_of_current_month.day)
            salary_date = current_date.replace(day=day_of_month)
            date_str = salary_date.strftime("%Y-%m-%d")
            amount = round(random.uniform(1500, 5000), 2)
            description = f"Salary Deposit"
            transactions.append(
                {
                    "date": date_str,
                    "description": description,
                    "category": salary_category,
                    "amount": amount,
                    "type": "income",
                }
            )
            salary_counts_per_month[year_month] += 1
        current_date += timedelta(days=32)
        current_date = current_date.replace(day=1)

    for _ in range(num_rows - len(transactions)):
        # Randomly select a date within the range
        random_days = random.randint(0, time_difference.days)
        transaction_date = start_date + timedelta(days=random_days)
        date_str = transaction_date.strftime("%Y-%m-%d")
        year_month = transaction_date.strftime("%Y-%m")

        # Ensure we don't exceed 2 salaries per month unintentionally
        if salary_counts_per_month[year_month] >= 2:
            category = random.choice(
                [cat for cat in categories if cat != salary_category]
            )
        else:
            category = random.choice(categories)

        # Determine transaction type based on category (simple heuristic)
        if any(keyword in category.lower() for keyword in income_keywords):
            transaction_type = "income"
        elif any(keyword in category.lower() for keyword in expense_keywords):
            transaction_type = "expense"
        else:
            transaction_type = random.choice(["income", "expense"])

        # Generate a description
        description_parts = [
            (
                random.choice(income_keywords)
                if transaction_type == "income"
                else random.choice(expense_keywords)
            )
        ]
        if random.random() < 0.6:
            description_parts.append(
                random.choice(["", " payment", " purchase", " deposit", " fee"])
            )
        description = (
            category.capitalize()
            + " "
            + "".join(description_parts).capitalize().strip()
        )

        # Generate a realistic amount
        if transaction_type == "income":
            if category == "Salary":
                amount = round(random.uniform(3000, 5000), 2)
            else:
                amount = round(random.uniform(50, 1000), 2)
        else:
            amount = round(random.uniform(1, 1500), 2)

        transactions.append(
            {
                "date": date_str,
                "description": description,
                "category": category,
                "amount": amount,
                "type": transaction_type,
            }
        )
        if category == salary_category:
            salary_counts_per_month[year_month] += 1

    return transactions


if __name__ == "__main__":
    start_date = "2024-01-01"
    end_date = "2025-04-30"
    num_transactions = 500
    possible_categories = [
        "Salary",
        "Rent",
        "Groceries",
        "Utilities",
        "Entertainment",
        "Transportation",
        "Freelance Income",
        "Food",
        "Shopping",
        "Investment Income",
        "Health",
        "Education",
        "Gifts",
        "Travel",
        "Bonus",
        "Other Income",
        "Other Expense",
    ]

    seed_data = generate_seed_data(
        start_date, end_date, num_transactions, possible_categories
    )

    sorted_seed_data = sorted(seed_data, key=lambda item: item["date"])

    with open("seed_data.json", "w") as f:
        json.dump(sorted_seed_data, f, indent=2)

    print(f"{len(seed_data)} rows of seed data generated and saved to seed_data.json")
