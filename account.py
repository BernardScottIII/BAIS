import datetime

class Account:
    def __init__(self, title:str, acct_type:str):
        self.title = title
        self.acct_type = acct_type
        self.ledger = f'/ledger/{title}.txt'
        self.cr_bal = 0
        self.dr_bal = 0
        self.bal_type = 'CR'
    
    def is_as(self):
        return self.acct_type == 'AS'
    
    def is_li(self):
        return self.acct_type == 'LI'
    
    def is_se(self):
        return self.acct_type == 'SE'
    
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