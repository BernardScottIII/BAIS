import datetime
import os
import inquirer
import account
import transaction

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
    dr_accts.append(account.Account(choice[0:choice.index(".")]))

for choice in cr_choice:
    cr_accts.append(account.Account(choice[0:choice.index(".")]))

# Change all of the ledger files to .csv and put headers in every one

trans_amnt = input("How much money will move between these accounts?\n>>>$")

print("When did this transaction occur?\nPlease enter in mm-dd-yyyy format.\n(Leave blank if today)")

month = input(">mm>>")
day = input(">dd>>")
year = input(">yyyy>>")

print(f"'{month}'")
print(f"'{day}'")
print(f"'{year}'")

if month == "":
    month = datetime.date.today().month
if year == "":
    year = datetime.date.today().year
if day == "":
    day = datetime.date.today().day

trans_date = datetime.date(int(year), int(month), int(day)).strftime('%b. %d %Y')

# Journalize the transaction

# Modify Transaction to use lists of accounts, instead of singletons
eco_event = transaction.Transaction()

# with open("general_journal.csv", "a+") as journal:
#     journal.writelines(f"{trans_date},{dr_acct},{cr_acct},${trans_amnt}\n")

# Post to ledger accounts
with open(f"ledger/{dr_acct}.txt", "a+") as dr_ledger:
    dr_ledger.writelines(f"{trans_date},{trans_amnt},\n")

with open(f"ledger/{cr_acct}.txt", "a+") as cr_ledger:
    cr_ledger.writelines(f"{trans_date},,{trans_amnt}\n")

# Prepare a trial balance
# Yeah we're going to need a list of acct's for users to select from
# Loop through the list
# apply a "get ledger bal" function
# put that into 