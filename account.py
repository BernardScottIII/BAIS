import datetime

class Account:
    def __init__(self, acc_type:str, title:str):
        self.title = title
        self.ledger = f'ledger/{acc_type}/{title}.txt'
        self.cr_bal = 0
        self.dr_bal = 0
        self.is_norm_bal = True
        self.type_of_acct = acc_type

    def __str__(self):
        return f"Account: {self.title}\nDebits: {self.dr_bal}\nCredits: {self.cr_bal}"
    
    def dr(self, amount:float, date:str=datetime.date.today().strftime('%b. %d %Y')):
        self.dr_bal += amount

        with open(self.ledger, "a+") as ledger:
            ledger.writelines(f"{date},{amount},,\n")
    
    def cr(self, amount:float, date:str=datetime.date.today().strftime('%b. %d %Y')):
        self.cr_bal += amount

        with open(self.ledger, "a+") as ledger:
            ledger.writelines(f",,{amount},{date}\n")

    def bal(self):
        debits = self.dr_bal
        credits = self.cr_bal
        if debits > credits:
            self.is_norm_bal = False
            return debits - credits
        elif credits > debits:
            self.is_norm_bal = True
            return credits - debits
        else:
            return 0

    def is_norm(self):
        return self.is_norm_bal
    
    def acct_type(self):
        return self.type_of_acct
    
    def acct_title(self):
        return self.title