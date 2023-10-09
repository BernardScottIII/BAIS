from account import Account
import os
import csv

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
                print(row)
                types[i].extend(row)
                print(types[i])
                i += 1

        self.categories = os.listdir(f"{filepath}/")
        self.accounts = []
        for category in self.categories:
            for acct in os.listdir(f"{filepath}/{category}"):
                debit_is_nomral = False
                if category in self.asset_accounts:
                    debit_is_nomral = True
                
                self.accounts.append(Account(category, acct[0:acct.index(".")], debit_is_nomral))

    def list_acct_titles(self):
        result = []
        for acct in self.accounts:
            result.append(f"{acct.acct_title()}")
        return result
    
    def get_accts(self):
        return self.accounts
    
    def get_categories(self):
        return self.categories
    
    def get_trial_bal(self):
        pass