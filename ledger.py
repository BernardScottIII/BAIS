from account import Account
import os
import csv
import copy

class Ledger:
    def __init__(self,
                 filepath:os.path,
                 breakdown:str):
        
        self.asset_accounts = []
        self.liability_accounts = []
        self.se_accounts = []

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
        with open("trial_balance.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Account", "Debit", "Credit"])
            dr_sum = 0
            cr_sum = 0
            for acct in self.accounts:
                if acct.get_bal_status() == "DEBIT":
                    writer.writerow([acct.acct_title(),acct.bal(),None])
                    dr_sum += acct.bal()
                else:
                    writer.writerow([acct.acct_title(),None,acct.bal()])
                    cr_sum += acct.bal()
            writer.writerow(["Totals", dr_sum, cr_sum])
    
    def original_sort(self, acct:Account):
        if acct.acct_title() in self.sorted_order:
            return self.sorted_order.index(acct.acct_title())
        else:
            return -1