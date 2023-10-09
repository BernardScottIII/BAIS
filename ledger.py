from account import Account
from transaction import Transaction
from datetime import date
import os

class Ledger:
    def __init__(self,
                 filepath:os.path,
                 asset_accts:list,
                 liability_accts:list,
                 se_accts:list):
        self.categories = os.listdir(f"{filepath}/")
        self.accounts = []
        for category in self.categories:
            for acct in os.listdir(f"{filepath}/{category}"):
                debit_is_nomral = False
                if category in asset_accts:
                    """        ^^ Some list of acct's """
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