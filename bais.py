import os
from datetime import date

print("""
+--------------------------------------------------+
| Starting Bernard's Accounting Information System |
+--------------------------------------------------+""")

if os.path.exists("general_journal.txt") == False:
    print("No general_journal.txt file found!\nShutting down.")
    exit()

num_entries = 2
account1 = ""
account2 = ""

while num_entries > 0:

    account_title = ""
    choice = input("""
Which part of a transaction would you like to record?
1. Assets
2. Liabilities
3. Stockholders' Equity
x. Exit
>>> """)

    if choice == "1":
        category = input("""
Which asset category would you like to record?
1. Cash
2. Supplies
3. Prepaid Insurance
4. Equipment
5. Accounts Receivable
>>> """)
        if category == "1":
            account_title = "cash"
        elif category == "2":
            account_title = "supplies"
        elif category == "3":
            account_title = "prepaid_insurance"
        elif category == "4":
            account_title = "equipment"
        elif category == "5":
            account_title = "accounts_receivable"
    elif choice == "2":
        category = input("""
Which Liability category would you like to record?
1. Notes Payable
2. Accounts Payable
3. Unearned Service Revenue
>>> """)
        if category == "1":
            account_title = "notes_payable"
        elif category == "2":
            account_title = "accounts_payable"
        elif category == "3":
            account_title = "unearned_service_revenue"
    elif choice == "3":
        category = input("""
Which Stockholders' Equity category would you like to record?
1. Common Stock
2. Service Revenue
3. Salaries and Wages Expense
4. Dividends
5. Rent Expense
>>> """)
        if category == "1":
            account_title = "common_stock"
        elif category == "2":
            account_title = "service_revenue"
        elif category == "3":
            account_title = "salaries_and_wages_expense"
        elif category == "4":
            account_title = "dividends"
        elif category == "5":
            account_title = "rent_expense"
    elif choice == "x":
        exit()

    # These inputs need to be checked so only numerical values are input
    # However, that is a thing future me will be burdened with
    
    amount = input(f"Insert value of {account_title} in dollars first, then cents\n>>>$").replace(",","")

    input_balance = float(amount)

    amount = amount.replace("-", "")
    
    credit_type = ""

    if choice in ['2', '3']:
        if input_balance > 0:
            credit_type = "credit"
        else:
            credit_type = "debit"
    else:
        if input_balance > 0:
            credit_type = "debit"
        else:
            credit_type = "credit"

    if num_entries > 1:
        account1 = f"{date.today().strftime('%b. %d %Y')},{account_title},{credit_type},{amount},"
    else:
        account2 = f"{account_title},{credit_type},{amount},"
            
    num_entries -= 1

explanation = input("Explanation for transaction:")

with open("general_journal.txt", "a+") as data:
        data.writelines(f"{account1}{account2}({explanation})\n")
        data.seek(0)
#         print(f"""
# Congratulations! You added a transaction to general_journal.txt!

# Contents of data.txt:
# {data.read()}""")

with open(f"ledger/{account1[account1.index(',')+1:account1.index(',', account1.index(',')+1)]}.txt", "a+") as ledger:
    ledger.writelines(f"{account1[account1.index(',', account1.index(',', account1.index(',')+1))+1:-1]}\n")
    # ledger.seek(0)
    # print(ledger.read())

with open(f"ledger/{account2[:account2.index(',', account2.index(','))]}.txt", "a+") as ledger:
    ledger.writelines(f"{account2[account2.index(',')+1:-1]}\n")
    # ledger.seek(0)
    # print(ledger.read())