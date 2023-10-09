from datetime import date
from account import Account
from transaction import Transaction
from ledger import Ledger
import os
import inquirer

print("""
+--------------------------------------------------+
| Starting Bernard's Accounting Information System |
+--------------------------------------------------+""")

# Create a Ledger object and tell it where all accounts are categorized and stored
general_ledger = Ledger("ledger")

options = general_ledger.get_accts()

# Print accounts for user to choose to debit or credit
dr_accts = inquirer.checkbox("Which account(s) are you debiting?", choices=options)

# Prevent user from crediting same account being debited
for acct in dr_accts:
    options.remove(acct)

cr_accts = [""]

# Logic to prevent user debiting AND crediting multiple accounts in single transaction
if len(dr_accts) > 1:
    cr_accts[0] = inquirer.list_input("Which account are you crediting?", choices=options)
else:
    cr_choice = inquirer.checkbox("Which account(s) are you crediting?", choices=options)

# Collect amounts user is debiting and crediting from each account
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

# Get other transaction information, like date and explanation
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

# Create Transaction object
transaction = Transaction(dr_accts, cr_accts, dr_amnts, cr_amnts, trans_date)

# Journalize the transaction and add optional explanation
transaction.journalize(input("(optional) Explanation for entry\n>>>"))

# Post transaction to ledger accounts
transaction.post()

# Prepare a trial balance
general_ledger.get_trial_bal()
for category in general_ledger.get_categories():
    for acct in os.listdir(f"ledger/{category}"):
        
        # Sum up all of debits
        dr_sum = 0
        with open(f"ledger/{category}/{acct}") as ledger:
            for line in ledger:
                # This line sucks
                dr_sum += int(line[line.index(",")+1:line.index(",",line.index(",")+1)])

        # Sum up all of credits

        # Get difference of dr-cr

        # If +, dr bal
        # If -, cr bal

        # report abs. val. and bal type

# List accts and balances in order
# Check if dr's == cr's