from datetime import date
from transaction import Transaction
from ledger import Ledger
import inquirer
import csv

print("""
+--------------------------------------------------+
| Starting Bernard's Accounting Information System |
+--------------------------------------------------+""")

# Cumulative list of journal entries, allowing for multiple transactions
journal_entries = []

# Create a Ledger object and tell it where all accounts are categorized and stored
general_ledger = Ledger("ledger", "ledger_breakdown.csv")

def create_entry(keyword:str):
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
        cr_accts = inquirer.checkbox("Which account(s) are you crediting?", choices=options)

    # Replace removed options in general ledger
    for acct in dr_accts:
        options.append(acct)
    options.sort(key=general_ledger.original_sort)

    # Collect amounts user is debiting and crediting from each account
    dr_amnts = []
    cr_amnts = []

    for acct in dr_accts:
        dr_amnts.append(
            float(
                input(f"Enter amount being debited to/from {acct.acct_title()}\n>>>$")
            )
        )

    for acct in cr_accts:
        cr_amnts.append(
            float(
                input(f"Enter amount being credited to/from {acct.acct_title()}\n>>>$")
            )
        )

    # Get other transaction information, including date and explanation
    print(f"When did this {keyword} occur?\nPlease enter in mm-dd-yyyy format.\n(Leave blank if today)")

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
    transaction.journalize(input(f"(optional) Explanation for {keyword}\n>>>"))

    # Add transaction to list of transactions to be posted to the ledger
    journal_entries.append(transaction)

# Post all transactions to the general ledger
def post_entries():
    for entry in journal_entries:
        entry.post()
        print(entry.summarize())

# Helper function to convert three character month code into its integer
# equivalent
def m_str_to_int(month:str):
    if "Jan" in month:
        return 1
    elif "Feb" in month:
        return 2
    elif "Mar" in month:
        return 3
    elif "Apr" in month:
        return 4
    elif "May" in month:
        return 5
    elif "Jun" in month:
        return 6
    elif "Jul" in month:
        return 7
    elif "Aug" in month:
        return 8
    elif "Sep" in month:
        return 9
    elif "Oct" in month:
        return 10
    elif "Nov" in month:
        return 11
    elif "Dec" in month:
        return 12
    else:
        return -1

def import_entries(filename:str):

    # Implementation of default value
    # Using the "=" convention in the argument does not work for some reason.
    if filename == "":
        filename = "general_journal.csv"

    with open(filename, "r", newline="") as journal:
        reader = csv.reader(journal)

        # Create empty fields for transaction information
        dr_accts = []
        cr_accts = []
        dr_amnts = []
        cr_amnts = []

        # Flag determining when complete transaction is read from journal
        trans_complete = False

        for row in reader:
            
            trans_date = date.today()
            explanation = ""

            # For every row in the csv file
            # Get the date at [0][0]
            if row[0] != "":
                year = int(row[0][7:])
                month = m_str_to_int(row[0][:3])
                day = int(row[0][5:7])
                trans_date = date(year, month, day)

            # If row[1] starts with '(', then an explanation is recorded
            if row[1].find("(") != -1:
                explanation = row[1][1:len(row[1])-1]
                trans_complete = True
            # If 2nd cell isn't empty, add a debit item
            elif row[1] != "":
                dr_accts.append(general_ledger.find_acct(row[1]))
                dr_amnts.append(float(row[4]))
            # Otherwise, add a credit item
            elif row[2] != "":
                cr_accts.append(general_ledger.find_acct(row[2]))
                cr_amnts.append(float(row[5]))

            # When the entire transaction has been read, create the object and
            # add it to the global journal entries list 
            if trans_complete == True:
                transaction = Transaction(dr_accts, cr_accts, dr_amnts, cr_amnts, trans_date, explanation)
                print(f"Adding: {transaction.summarize()}")
                journal_entries.append(transaction)

                # Reset flag for new transaction
                trans_complete = False

                # Clear transaction information lists
                dr_accts = []
                cr_accts = []
                dr_amnts = []
                cr_amnts = []

# Main program loop
choice = ""
while choice != "Exit":
    main_menu_options = ["Import Journal Entries",
                        "Create Journal Entry",
                        "Post all Journal Entries",
                        "Prepare Trial Balance",
                        "Adjust Journal Entries",
                        "Exit"]
    choice = inquirer.list_input("Main Menu", choices=main_menu_options)

    if choice == "Create Journal Entry":
        create_entry("transaction")
    elif choice == "Post all Journal Entries":
        post_entries()
    elif choice == "Prepare Trial Balance":
        general_ledger.get_trial_bal()
        print("Trial Balance Generated!")
    elif choice == "Adjust Journal Entries":
        create_entry("adjustment")
    elif choice == "Import Journal Entries":
        file = input("Enter path/name of journal file (Default: general_journal.csv)\n>>>")
        import_entries(file)