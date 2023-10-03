import datetime

class Account:
    def __init__(self, title:str):
        self.title = title
        self.ledger = f'ledger/{title}.txt'
        self.cr_bal = 0
        self.dr_bal = 0
        self.bal_is_cr = True

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
            self.bal_is_cr = False
            return debits - credits
        elif credits > debits:
            self.bal_is_cr = True
            return credits - debits
        else:
            return 0

    def bal_type(self):
        return self.bal_is_cr
    
    def acct_title(self):
        return self.title