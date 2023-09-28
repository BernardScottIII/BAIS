import datetime

print("""
+--------------------------------------------------+
| Starting Bernard's Accounting Information System |
+--------------------------------------------------+""")

debit_acct = input("Which account are you debiting?\n>>>")
credit_acct = input("Which account are you crediting?\n>>>")
trans_amnt = input("How much money will move between these accounts?\n>>>$")

print("When did this transaction occur?\nPlease enter in mm-dd-yyyy format.\n(Leave blank if today)")

month = input(">mm>>")
day = input(">dd>>")
year = input(">yyyy>>")

print(f"'{month}'")
print(f"'{day}'")
print(f"'{year}'")

if month == "":
    month = datetime.date.today().month
if year == "":
    year = datetime.date.today().year
if day == "":
    day = datetime.date.today().day

trans_date = datetime.date(int(year), int(month), int(day)).strftime('%b. %d %Y')

print(debit_acct)
print(credit_acct)
print(trans_amnt)
print(trans_date)