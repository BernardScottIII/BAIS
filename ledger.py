from account import Account
import os
import csv

class Ledger:
    def __init__(self,
                 filepath:os.path,
                 breakdown:str):
        
        # Take rows from breakdown and relate them to a part of the basic
        # accounting equation
        self.asset_accounts = []
        self.liability_accounts = []
        self.se_accounts = []

        types = [self.asset_accounts, self.liability_accounts, self.se_accounts]

        with open(breakdown, "r") as bd:
            i = 0
            for row in csv.reader(bd):
                types[i].extend(row)
                i += 1

        # Created to help break down ledger files
        self.categories = os.listdir(f"{filepath}/")
        
        # Make each file in the ledger filepath its own Account object
        self.accounts = []

        # Created for re-ordering accounts when order is broken
        self.sorted_order = []

        for category in self.categories:
            for acct in os.listdir(f"{filepath}/{category}"):
                self.accounts.append(Account(category, acct[0:acct.index(".")]))
                self.sorted_order.append(acct[0:acct.index(".")])

    # Return list[str] of title of every account in every category in ledger
    def list_acct_titles(self):
        result = []
        for acct in self.accounts:
            result.append(f"{acct.acct_title()}")
        return result
    
    # Return reference to list of accounts in ledger
    def get_accts(self):
        return self.accounts
    
    # Create current trial balance with every account in ledger
    def get_trial_bal(self):
        with open("trial_balance.csv", "w", newline="") as tb:
            writer = csv.writer(tb)
            writer.writerow(["Account", "Debit", "Credit"])

            dr_total = 0
            cr_total = 0
            for acct in self.accounts:
                # Open each account's ledger
                with open(acct.ledger, "r", newline="") as ledger:
                    reader = csv.reader(ledger)

                    # Sum up all credits and debits in the account's ledger
                    dr_bal = 0
                    cr_bal = 0
                    for row in reader:
                        if row[1] != "":
                            dr_bal += float(row[1])
                        else:
                            cr_bal += float(row[2])

                    # Determine if balance is debit or credit balance, and add
                    # to trial_balance.csv accordingly
                    if dr_bal > cr_bal:
                        writer.writerow([acct.acct_title(),(dr_bal - cr_bal),None])
                        dr_total += (dr_bal - cr_bal)
                    else:
                        writer.writerow([acct.acct_title(),None,(cr_bal - dr_bal)])
                        cr_total += (cr_bal - dr_bal)
            
            # Write total debit and credit balances as last row
            writer.writerow(["Totals",dr_total,cr_total])
    
    # Sort list of accounts back into original order
    def original_sort(self, acct:Account):
        if acct.acct_title() in self.sorted_order:
            return self.sorted_order.index(acct.acct_title())
        else:
            return -1
    
    # Given a valid account title, return a reference to that account
    def find_acct(self, acct_name:str):
        return self.accounts[self.sorted_order.index(acct_name)]