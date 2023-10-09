from account import Account
import os
import csv
import copy

class Ledger:
    def __init__(self,
                 filepath:os.path,
                 breakdown:str,
                 journal:str="general_journal.csv"):
        
        self.asset_accounts = []
        self.liability_accounts = []
        self.se_accounts = []

        self.journal = journal

        types = [self.asset_accounts, self.liability_accounts, self.se_accounts]

        with open(breakdown, "r") as bd:
            i = 0
            for row in csv.reader(bd):
                types[i].extend(row)
                i += 1

        self.categories = os.listdir(f"{filepath}/")
        self.accounts = []
        self.sorted_order = []
        for category in self.categories:
            for acct in os.listdir(f"{filepath}/{category}"):
                debit_is_nomral = False
                if category in self.asset_accounts:
                    debit_is_nomral = True
                
                self.accounts.append(Account(category, acct[0:acct.index(".")], debit_is_nomral))
                self.sorted_order.append(acct[0:acct.index(".")])

    def list_acct_titles(self):
        result = []
        for acct in self.accounts:
            result.append(f"{acct.acct_title()}")
        return result
    
    def get_accts(self):
        return self.accounts
    
    def get_categories(self):
        return copy.deepcopy(self.categories)
    
    def get_trial_bal(self):
        with open("trial_balance.csv", "w", newline="") as tb:
            writer = csv.writer(tb)
            writer.writerow(["Account", "Debit", "Credit"])
            dr_total = 0
            cr_total = 0
            for acct in self.accounts:
                print(acct.acct_title())
                with open(acct.ledger, "r", newline="") as ledger:
                    reader = csv.reader(ledger)

                    # Sum up all credits and debits in the account's ledger
                    dr_bal = 0
                    cr_bal = 0
                    for row in reader:
                        if row[1] != "":
                            dr_bal += int(row[1])
                        else:
                            cr_bal += int(row[2])

                    if dr_bal > cr_bal:
                        writer.writerow([acct.acct_title(),(dr_bal - cr_bal),None])
                        dr_total += (dr_bal - cr_bal)
                    else:
                        writer.writerow([acct.acct_title(),None,(cr_bal - dr_bal)])
                        cr_total += (cr_bal - dr_bal)
            writer.writerow(["Totals",dr_total,cr_total])
                


    
    def original_sort(self, acct:Account):
        if acct.acct_title() in self.sorted_order:
            return self.sorted_order.index(acct.acct_title())
        else:
            return -1