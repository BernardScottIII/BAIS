from datetime import date
from account import Account
from ledger import Ledger

class Transaction:
    def __init__(self,
                 acct_dr:Account,
                 acct_cr:Account,
                 dr_amnts:list,
                 cr_amnts:list,
                 date:date=date.today().strftime('%b. %d %Y'),
                 explanation:str='unexplained entry',
                 default_journal:str='general_journal.csv'):
        
        self.acct_dr = []
        self.acct_cr = []
        self.amount = []

        i = 0
        for acct in acct_dr:
            self.acct_dr.append(Item(acct,dr_amnts[i]))
            i += 1
        
        i = 0
        for acct in acct_cr:
            self.acct_cr.append(Item(acct,cr_amnts[i]))
            i += 1

        self.explanation = explanation
        self.date = date.strftime('%b. %d %Y')
        self.default_journal = default_journal

    def dr_items(self):
        result = ""
        for acct in self.acct_dr:
            result += f",{acct.title()},,,{acct.amount()},\n"
        return result
    
    def cr_items(self):
        result = ""
        for acct in self.acct_cr:
            result += f",,{acct.title()},,,{acct.amount()}\n"
        return result

    def journalize(self, explanation:str):
        if explanation is None or explanation == "":
            explanation = self.explanation
        else:
            self.explanation = explanation

        with open(self.default_journal, "a+") as journal:
            journal.writelines(f"{self.date}{self.dr_items()}{self.cr_items()},({self.explanation})\n")

    def post(self):
        for item in self.acct_dr:
            item.account().dr(item.amount(), self.date)
        for item in self.acct_cr:
            item.account().cr(item.amount(), self.date)
        
    def summarize(self):
        result = "Transaction: "
        for item in self.acct_dr:
            result += f"{item.title()}, "
        result += " <==> "
        for item in self.acct_cr:
            result += f"{item.title()}, "
        return result

class Item:
    def __init__(self,
                 acct:Account,
                 amnt:float):
        self.acct = acct
        self.amnt = amnt
    
    def title(self):
        return self.acct.acct_title()
    
    def amount(self):
        return self.amnt
    
    def account(self):
        return self.acct