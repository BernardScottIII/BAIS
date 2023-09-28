import datetime
import account

class Transaction:
    def __init__(self,
                 acct_dr:account,
                 acct_cr:account,
                 amount:float,
                 date:datetime.date=datetime.date.today().strftime('%b. %d %Y'),
                 explanation:str='unexplained entry',
                 default_journal:str='general_journal.txt'):
        
        self.acct_dr = acct_dr
        self.acct_cr = acct_cr
        self.amount = amount

        self.explanation = explanation
        self.date = date.strftime('%b. %d %Y')
        self.default_journal = default_journal
    
    def journalize(self):
        with open(self.default_journal, "a+") as data:
            data.writelines(f"{self.date},{self.acct_dr},{self.amount},{self.acct_cr},{self.amount},({self.explanation})\n")
    
    def post(self):
        self.acct_dr.dr(self.amount, self.date)
        self.acct_cr.cr(self.amount, self.date)
