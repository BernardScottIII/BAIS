from datetime import date
import copy
import csv

class Account:
    def __init__(self, acc_type:str, title:str):
        self.title = title
        self.ledger = f'ledger/{acc_type}/{title}.csv'
        self.cr_bal = 0
        self.dr_bal = 0
        self.type_of_acct = acc_type

    def __str__(self):
        return f"Account: {self.title}"
    
    # Create a debit post on this account's ledger
    def dr(self, amount:float, date:str=date.today().strftime('%b. %d %Y')):
        self.dr_bal += amount
        with open(self.ledger, "a+", newline="") as ledger:
            writer = csv.writer(ledger)
            writer.writerow([date,amount,"",""])
    
    # Create a credit post on this account's ledger
    def cr(self, amount:float, date:str=date.today().strftime('%b. %d %Y')):
        self.cr_bal += amount
        with open(self.ledger, "a+", newline="") as ledger:
            writer = csv.writer(ledger)
            writer.writerow(["","",amount, date])

    # Return outstanding balance of account
    def bal(self):
        return abs(self.dr_bal-self.cr_bal)
    
    # Return which category this account belongs to
    def type(self):
        return copy.deepcopy(self.type_of_acct)
    
    # Return title of account
    def acct_title(self):
        return copy.deepcopy(self.title)