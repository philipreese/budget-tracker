# budget-tracker

## Command Line Interface

usage: budget_cli.py [-h] {add-income,add-expense,delete-transactions,view-summary} ...

Budget Tracker CLI

positional arguments:
{add-income,add-expense,delete-transactions,view-summary}

|       command       |        description         |
| :-----------------: | :------------------------: |
|     add-income      | Add an income transaction  |
|     add-expense     | Add an expense transaction |
| delete-transactions |  Delete all transactions   |
|    view-summary     |  View transaction summary  |

options:
-h, --help show this help message and exit

### add-income

usage: budget_cli.py add-income [-h] [-d DATE] -a AMOUNT [-c CATEGORY] [-desc DESCRIPTION]

|             options              |                   description                   |
| :------------------------------: | :---------------------------------------------: |
|            -h, --help            |         show this help message and exit         |
|         -d, --date DATE          | Transaction date (YYYY-MM-DD), default is today |
|       -a, --amount AMOUNT        |               Transaction amount                |
|     -c, --category CATEGORY      |              Transaction category               |
| -desc, --description DESCRIPTION |             Transaction description             |

### add-expense

usage: budget_cli.py add-expense [-h] [-d DATE] -a AMOUNT [-c CATEGORY] [-desc DESCRIPTION]

|             options              |                   description                   |
| :------------------------------: | :---------------------------------------------: |
|            -h, --help            |         show this help message and exit         |
|         -d, --date DATE          | Transaction date (YYYY-MM-DD), default is today |
|       -a, --amount AMOUNT        |               Transaction amount                |
|     -c, --category CATEGORY      |              Transaction category               |
| -desc, --description DESCRIPTION |             Transaction description             |

### delete-transactions

usage: budget_cli.py delete-transactions [-h]

options:
-h, --help show this help message and exit

### view-summary

usage: budget_cli.py view-summary [-h]

options:
-h, --help show this help message and exit
