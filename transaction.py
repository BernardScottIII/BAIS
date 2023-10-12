from datetime import date
from account import Account
import csv

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

        # Turn every account into an item within the transaction
        i = 0
        for acct in acct_dr:
            self.acct_dr.append(Item(acct,dr_amnts[i]))
            i += 1
        
        i = 0
        for acct in acct_cr:
            self.acct_cr.append(Item(acct,cr_amnts[i]))
            i += 1

        # Assignment of optional arguments
        self.explanation = explanation
        self.date = date.strftime('%b. %d %Y')
        self.default_journal = default_journal

    # Returns .csv formatted debits of transaction
    def dr_items(self):
        result = []
        for acct in self.acct_dr:
            result.append(["",acct.title(),"","",acct.amount(),""])
        return result
    
    # Returns .csv formatted credits of transaction
    def cr_items(self):
        result = []
        for acct in self.acct_cr:
            result.append(["","",acct.title(),"","",acct.amount()])
        return result

    # Writes the date, accounts debited, accounts credited, amounts debited,
    # amounts credited, and the explanation for the current transaction 
    def journalize(self, explanation:str):
        # Record explanation for transaction
        if explanation is None or explanation == "":
            explanation = self.explanation
        else:
            self.explanation = explanation

        # Gather .csv rows containing debit and credit info
        entries = []
        entries.extend(self.dr_items())
        entries.extend(self.cr_items())
        entries.extend([["",f"({self.explanation})"]])

        print(entries)

        # Insert date into appropriate cell
        entries[0][0] = self.date

        # Execute the write to the .csv file
        with open(self.default_journal, "a+", newline="") as journal:
            writer = csv.writer(journal)
            writer.writerows(entries)

    # Post debits and credits to ledger accounts by writing data to .csv files
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