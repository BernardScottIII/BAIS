from datetime import date
from transaction import Transaction
from ledger import Ledger
import inquirer

print("""
+--------------------------------------------------+
| Starting Bernard's Accounting Information System |
+--------------------------------------------------+""")

# Create a Ledger object and tell it where all accounts are categorized and stored
general_ledger = Ledger("ledger", "ledger_breakdown.csv")

# Create local reference to general ledger's list of accounts
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

# Replace removed options in general ledger
for acct in dr_accts:
    options.append(acct)
options.sort(key=general_ledger.original_sort)

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

# Get other transaction information, including date and explanation
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

# Post transaction to the general ledger
transaction.post(general_ledger)

# Prepare a trial balance
general_ledger.get_trial_bal()