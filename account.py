import datetime

class Account:
    def __init__(self, title:str):
        self.title = title
        self.ledger = f'/ledger/{title}.txt'
        self.cr_bal = 0
        self.dr_bal = 0
        self.bal_type = 'CR'

    def __str__(self):
        return f"Account: {self.title}\nDebits: {self.dr_bal}\nCredits: {self.cr_bal}"
    
    def cr(self, amount:float, date:datetime.date=datetime.date.today().strftime('%b. %d %Y')):
        date = date.strftime('%b. %d %Y')
        self.cr_bal += amount

    def dr(self, amount:float, date:datetime.date=datetime.date.today().strftime('%b. %d %Y')):
        date = date.strftime('%b. %d %Y')
        self.dr_bal += amount

    def bal(self):
        pass

    def get_bal_type(self):
        return self.bal_type