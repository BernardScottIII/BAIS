from datetime import date
import copy

class Account:
    def __init__(self, acc_type:str, title:str, dr_norm:bool=False):
        self.title = title
        self.ledger = f'ledger/{acc_type}/{title}.txt'
        self.cr_bal = 0
        self.dr_bal = 0
        self.type_of_acct = acc_type
        self.dr_is_norm_bal = dr_norm
        self.bal_status = ""
        self.update_bal_status()

    def __str__(self):
        return f"Account: {self.title}"
    
    def dr(self, amount:float, date:str=date.today().strftime('%b. %d %Y')):
        self.dr_bal += amount
        self.update_bal_status()
        with open(self.ledger, "a+") as ledger:
            ledger.writelines(f"{date},{amount},,\n")
    
    def cr(self, amount:float, date:str=date.today().strftime('%b. %d %Y')):
        self.cr_bal += amount
        self.update_bal_status()
        with open(self.ledger, "a+") as ledger:
            ledger.writelines(f",,{amount},{date}\n")

    def bal(self):
        return abs(self.dr_bal-self.cr_bal)
    
    def type(self):
        return copy.deepcopy(self.type_of_acct)
    
    def acct_title(self):
        return copy.deepcopy(self.title)
    
    def norm_bal_is_dr(self):
        return copy.deepcopy(self.dr_is_norm_bal)
    
    def update_bal_status(self):
        if self.dr_is_norm_bal:
            if self.dr_bal > self.cr_bal:
                self.bal_status = "DEBIT"
            elif self.cr_bal > self.dr_bal:
                self.bal_status = "CREDIT"
            else:
                self.bal_status = "DEBIT"
        else:
            if self.dr_bal > self.cr_bal:
                self.bal_status = "CREDIT"
            elif self.cr_bal > self.dr_bal:
                self.bal_status = "DEBIT"
            else:
                self.bal_status = "CREDIT"

    def get_bal_status(self):
        return copy.deepcopy(self.bal_status)