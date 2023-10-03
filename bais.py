from datetime import date
from account import Account
from transaction import Transaction
import os
import inquirer

print("""
+--------------------------------------------------+
| Starting Bernard's Accounting Information System |
+--------------------------------------------------+""")

files = os.listdir("ledger/")
dr_choice = inquirer.checkbox("Which account are you debiting?", choices=files)
for acct in dr_choice:
    files.remove(acct)

cr_choice = [""]

if len(dr_choice) > 1:
    cr_choice[0] = inquirer.list_input("Which account are you crediting?", choices=files)
else:
    cr_choice = inquirer.checkbox("Which account are you crediting?", choices=files)

for acct in cr_choice:
    files.remove(acct)

dr_accts = []
cr_accts = []

for choice in dr_choice:
    dr_accts.append(Account(choice[0:choice.index(".")]))

for choice in cr_choice:
    cr_accts.append(Account(choice[0:choice.index(".")]))

# Change all of the ledger files to .csv and put headers in every one

dr_amnts = []
cr_amnts = []

for acct in dr_accts:
    dr_amnts.append(
        int(
            input(f"Enter amount being debited to/from {acct.acct_title()}\n>>>$")
        )
    )

for acct in cr_accts:
    cr_amnts.append(
        int(
            input(f"Enter amount being credited to/from {acct.acct_title()}\n>>>$")
        )
    )

print("When did this transaction occur?\nPlease enter in mm-dd-yyyy format.\n(Leave blank if today)")

month = input(">mm>>")
day = input(">dd>>")
year = input(">yyyy>>")

today = date.today()

if month == "":
    month = today.month
if year == "":
    year = today.year
if day == "":
    day = today.day

trans_date = date(int(year), int(month), int(day))

# Create transaction
transaction = Transaction(dr_accts, cr_accts, dr_amnts, cr_amnts, trans_date)

# Journalize the transaction
transaction.journalize(input("(optional) Explanation for entry\n>>>"))

# Post to ledger accounts
transaction.post()

# Prepare a trial balance
# apply a "get ledger bal" function
# put that into 