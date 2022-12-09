import bank
import csv
import datetime
import decimal

class RBC(bank.Bank):
    def __init__(self):
        bank.Bank.__init__(self)
        
    def add(self, file):
        with open(file, "r") as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quoting=csv.QUOTE_ALL)
            next(reader) # Skip header
            for row in reader:
                entry = None
                
                desc=self.filter_desc(row[5])
                if(len(desc) ==0):
                    desc = self.filter_desc(row[4])
                if(row[0].startswith("Visa")):
                    entry = (datetime.datetime.strptime(row[2], "%m/%d/%Y"), False, desc, decimal.Decimal(row[6])*-1)
                elif(self.remove_accents(row[0]).startswith("Cheque") or row[0].startswith("Check")):
                    entry = (datetime.datetime.strptime(row[2], "%m/%d/%Y"), True, desc, decimal.Decimal(row[6]))
                
                if(entry):
                    self.entries.append(entry)
