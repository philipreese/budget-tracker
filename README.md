# budget-tracker

- [budget-tracker](#budget-tracker)
  - [Command Line Interface](#command-line-interface)
    - [add-income](#add-income)
    - [add-expense](#add-expense)
    - [get-transaction](#get-transaction)
    - [get-transactions](#get-transactions)
    - [view-summary](#view-summary)
    - [edit-transaction](#edit-transaction)
    - [delete-transaction](#delete-transaction)
    - [configure](#configure)
    - [export-csv](#export-csv)
    - [plot-expenses](#plot-expenses)
  - [REST API](#rest-api)
    - [**POST** `/income/` Add Income](#post-income-add-income)
    - [**GET** `/income/` Get Income](#get-income-get-income)
    - [**POST** `/expenses/` Add Expense](#post-expenses-add-expense)
    - [**GET** `/expenses/` Get Expense](#get-expenses-get-expense)
    - [**GET** `/summary/` Get Summary](#get-summary-get-summary)
    - [**GET** `/export/csv/` Export Csv](#get-exportcsv-export-csv)

## Command Line Interface

All commands can be run with `pixi run cli ...` from the root level rather than

```
cd cli
python -m main.py ...
```

usage: budget_cli.py [-h] {add-income,add-expense,get-transaction,get-transactions,view-summary,edit-transaction,delete-transaction,configure,export-csv,plot-expenses}

| positional argument |                description                 |
| :-----------------: | :----------------------------------------: |
|     add-income      |         Add an income transaction          |
|     add-expense     |         Add an expense transaction         |
|   get-transaction   |       Get a single transaction by ID       |
|  get-transactions   | Get all transactions with optional filters |
|    view-summary     |          View transaction summary          |
|  edit-transaction   |        Edit an existing transaction        |
| delete-transaction  |          Delete transaction by id          |
|      configure      |         Change configuration items         |
|     export-csv      |         Export transactions to CSV         |
|    plot-expenses    |         Plot expenses by category          |

|   option   |           description           |
| :--------: | :-----------------------------: |
| -h, --help | show this help message and exit |

### add-income

usage: budget_cli.py add-income [-h] [-d DATE] -a AMOUNT [-c CATEGORY] [-desc DESCRIPTION]

|              option              |                    description                     |
| :------------------------------: | :------------------------------------------------: |
|            -h, --help            |          show this help message and exit           |
|       -a, --amount AMOUNT        |                 Transaction amount                 |
|         -d, --date DATE          |  Transaction date (YYYY-MM-DD), default is today   |
|     -c, --category CATEGORY      |      Transaction category, default is "Other"      |
| -desc, --description DESCRIPTION | Transaction description, default is "Other Income" |

### add-expense

usage: budget_cli.py add-expense [-h] [-d DATE] -a AMOUNT [-c CATEGORY] [-desc DESCRIPTION]

|              option              |                     description                     |
| :------------------------------: | :-------------------------------------------------: |
|            -h, --help            |           show this help message and exit           |
|       -a, --amount AMOUNT        |                 Transaction amount                  |
|         -d, --date DATE          |   Transaction date (YYYY-MM-DD), default is today   |
|     -c, --category CATEGORY      |      Transaction category, default is "Other"       |
| -desc, --description DESCRIPTION | Transaction description, default is "Other Expense" |

### get-transaction

usage: budget_cli.py get-transaction [-h] id

| positional argument |      description      |
| :-----------------: | :-------------------: |
|   transaction_id    | ID of the transaction |

|   option   |           description           |
| :--------: | :-----------------------------: |
| -h, --help | show this help message and exit |

### get-transactions

usage: budget_cli.py get-transactions [-h] [-s START_DATE] [-e END_DATE] [-c CATEGORY] [-t {income,expense}] [-o {date,desc,cat,amt,type}] [-od {asc,desc}]

|                 option                  |                         description                         |
| :-------------------------------------: | :---------------------------------------------------------: |
|               -h, --help                |               show this help message and exit               |
|       -s, --start-date START_DATE       |     Get transactions starting at this date (YYYY-MM-DD)     |
|         -e, --end-date END_DATE         | Get transactions up to and including this date (YYYY-MM-DD) |
|         -c, --category CATEGORY         |               Filter transactions by category               |
|       -t, --type {income,expense}       |                Get transactions of this type                |
| -o, --order-by {date,desc,cat,amt,type} |                 Sort transactions by column                 |
|    -od, --order-direction {asc,desc}    |       Sort order (ascending (default) or descending)        |

### view-summary

usage: budget_cli.py view-summary [-h] [-m MONTH] [-y YEAR] [-c CATEGORY] [-e] [-i]

|         option          |                         description                          |
| :---------------------: | :----------------------------------------------------------: |
|       -h, --help        |               show this help message and exit                |
|    -m, --month MONTH    | Filter summary by month (YYYY-MM or MM if also using --year) |
|     -y, --year YEAR     |                Filter summary by year (YYYY)                 |
| -c, --category CATEGORY |                  Filter summary by category                  |
|      -e, --expense      |      Show expense summary by category, default is False      |
|      -i, --income       |      Show income summary by category, default is False       |

### edit-transaction

usage: budget_cli.py edit-transaction [-h] [-d DATE] [-desc DESCRIPTION] [-c CATEGORY] [-a AMOUNT] [-t {INCOME,EXPENSE}] transaction_id

| positional argument |          description          |
| :-----------------: | :---------------------------: |
|   transaction_id    | ID of the transaction to edit |

|              option              |            description            |
| :------------------------------: | :-------------------------------: |
|            -h, --help            |  show this help message and exit  |
|         -d, --date DATE          | New transaction date (YYYY-MM-DD) |
| -desc, --description DESCRIPTION |    New transaction description    |
|     -c, --category CATEGORY      |     New transaction category      |
|       -a, --amount AMOUNT        |      New transaction amount       |
|   -t, --type {INCOME,EXPENSE}    |       New transaction type        |

### delete-transaction

usage: budget_cli.py delete-transaction [-h] transaction_id

| positional argument |                              description                               |
| :-----------------: | :--------------------------------------------------------------------: |
|   transaction_id    | ID of the transaction to delete. If ID is -1, deletes ALL transactions |

|   option   |           description           |
| :--------: | :-----------------------------: |
| -h, --help | show this help message and exit |

### configure

usage: budget_cli.py configure [-h] [-p DB_PATH] [-c CURRENCY_SYMBOL]

|          positional argument          |          description          |
| :-----------------------------------: | :---------------------------: |
|         -p, --db_path DB_PATH         | The path to the database file |
| -c, --currency-symbol CURRENCY_SYMBOL |  The currency symbol to use   |

|   option   |           description           |
| :--------: | :-----------------------------: |
| -h, --help | show this help message and exit |

### export-csv

usage: budget_cli.py export-csv [-h] [-s START_DATE] [-e END_DATE] [-c CATEGORY] [-f FILENAME] [-o {date,desc,cat,amt,type}] [-od {asc,desc}]

|                 option                  |                  description                   |
| :-------------------------------------: | :--------------------------------------------: |
|               -h, --help                |        show this help message and exit         |
|       -s, --start-date START_DATE       |     Start date for filtering (YYYY-MM-DD)      |
|         -e, --end-date END_DATE         |      End date for filtering (YYYY-MM-DD)       |
|         -c, --category CATEGORY         |             Category to filter by              |
|         -f, --filename FILENAME         |      The filename of the CSV to export to      |
| -o, --order-by {date,desc,cat,amt,type} |          Sort transactions by column           |
|    -od, --order-direction {asc,desc}    | Sort order (ascending (default) or descending) |

### plot-expenses

usage: budget_cli.py plot-expenses [-h] [-m MONTH]

|      option       |            description             |
| :---------------: | :--------------------------------: |
|    -h, --help     |  show this help message and exit   |
| -m, --month MONTH | Filter expenses by month (YYYY-MM) |

## REST API

### **POST** `/income/` Add Income

Example:

```
curl -X 'POST' \
  'http://localhost:8000/income/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "date": "2025-04-16",
    "description": "string",
    "category": "string",
    "amount": 0
    }'
```

### **GET** `/income/` Get Income

Example:

```
curl -X 'GET' \
  'http://localhost:8000/income/?date=2025-03' \
  -H 'accept: application/json'
```

### **POST** `/expenses/` Add Expense

Example:

```
curl -X 'POST' \
  'http://localhost:8000/expenses/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "date": "2025-04-16",
    "description": "string",
    "category": "string",
    "amount": 0
    }'
```

### **GET** `/expenses/` Get Expense

Example:

```
curl -X 'GET' \
  'http://localhost:8000/expenses/?date=2025-03&category=Groceries' \
  -H 'accept: application/json'
```

### **GET** `/summary/` Get Summary

Example:

```
curl -X 'GET' \
  'http://localhost:8000/summary/?date=2025-03' \
  -H 'accept: application/json'
```

### **GET** `/export/csv/` Export Csv

Example:

```
curl -X 'GET' \
  'http://localhost:8000/export/csv/?start_date=2025-01-01&end_date=2025-03-05&category=Groceries&filename=output.csv&order_by=amt&order_direction=asc' \
  -H 'accept: application/json'
```
