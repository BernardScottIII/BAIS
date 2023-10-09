from datetime import date

class Account:
    def __init__(self, acc_type:str, title:str, dr_norm:bool=False):
        self.title = title
        self.ledger = f'ledger/{acc_type}/{title}.txt'
        self.cr_bal = 0
        self.dr_bal = 0
        self.type_of_acct = acc_type
        self.dr_is_norm_bal = dr_norm

    def __str__(self):
        return f"Account: {self.title}"
    
    def dr(self, amount:float, date:str=date.today().strftime('%b. %d %Y')):
        self.dr_bal += amount

        with open(self.ledger, "a+") as ledger:
            ledger.writelines(f"{date},{amount},,\n")
    
    def cr(self, amount:float, date:str=date.today().strftime('%b. %d %Y')):
        self.cr_bal += amount

        with open(self.ledger, "a+") as ledger:
            ledger.writelines(f",,{amount},{date}\n")

    def bal(self):
        return abs(self.dr_bal-self.cr_bal)
    
    def type(self):
        return self.type_of_acct
    
    def acct_title(self):
        return self.title