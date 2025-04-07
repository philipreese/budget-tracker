from enum import Enum


class TransactionType(Enum):
    INCOME = "income"
    EXPENSE = "expense"

    def __str__(self):
        return self.value
