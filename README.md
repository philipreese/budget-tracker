# budget-tracker

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

usage: budget_cli.py get-transactions [-h] [-s START_DATE] [-e END_DATE] [-c CATEGORY] [-o {date,desc,cat,amt,type}] [-od {asc,desc}]

|                 option                  |                         description                         |
| :-------------------------------------: | :---------------------------------------------------------: |
|               -h, --help                |               show this help message and exit               |
|       -s, --start-date START_DATE       |     Get transactions starting at this date (YYYY-MM-DD)     |
|         -e, --end-date END_DATE         | Get transactions up to and including this date (YYYY-MM-DD) |
|         -c, --category CATEGORY         |               Filter transactions by category               |
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