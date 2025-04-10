# budget-tracker

## Command Line Interface

usage: budget_cli.py [-h] {add-income,add-expense,get-transaction,view-summary,edit-transaction,delete-transaction}

| positional argument |                           description                           |
| :-----------------: | :-------------------------------------------------------------: |
|     add-income      |                    Add an income transaction                    |
|     add-expense     |                   Add an expense transaction                    |
|   get-transaction   |                 Get a single transaction by ID                  |
|    view-summary     |                    View transaction summary                     |
|  edit-transaction   |                  Edit an existing transaction                   |
| delete-transaction  | Delete transaction by id. If ID is -1, deletes ALL transactions |

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
|     -c, --category CATEGORY      |      Transaction category, default is "other"      |
| -desc, --description DESCRIPTION | Transaction description, default is "other income" |

### add-expense

usage: budget_cli.py add-expense [-h] [-d DATE] -a AMOUNT [-c CATEGORY] [-desc DESCRIPTION]

|              option              |                     description                     |
| :------------------------------: | :-------------------------------------------------: |
|            -h, --help            |           show this help message and exit           |
|       -a, --amount AMOUNT        |                 Transaction amount                  |
|         -d, --date DATE          |   Transaction date (YYYY-MM-DD), default is today   |
|     -c, --category CATEGORY      |      Transaction category, default is "other"       |
| -desc, --description DESCRIPTION | Transaction description, default is "other expense" |

### get-transaction
usage: budget_cli.py get-transaction [-h] id

| positional argument |      description      |
| :-----------------: | :-------------------: |
|   transaction_id    | ID of the transaction |

|   option   |           description           |
| :--------: | :-----------------------------: |
| -h, --help | show this help message and exit |


### view-summary

usage: budget_cli.py view-summary [-h] [-m MONTH] [-y YEAR] [-c CATEGORY]

|         option          |                         description                          |
| :---------------------: | :----------------------------------------------------------: |
|       -h, --help        |               show this help message and exit                |
|    -m, --month MONTH    | Filter summary by month (YYYY-MM or MM if also using --year) |
|     -y, --year YEAR     |                Filter summary by year (YYYY)                 |
| -c, --category CATEGORY |                  Filter summary by category                  |

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

| positional argument |           description           |
| :-----------------: | :-----------------------------: |
|   transaction_id    | ID of the transaction to delete |

|   option   |           description           |
| :--------: | :-----------------------------: |
| -h, --help | show this help message and exit |