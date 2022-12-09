import bank
import csv
import datetime
import decimal

class AccesD(bank.Bank):
    def __init__(self):
        bank.Bank.__init__(self)
    
    def add(self, file):
        with open(file, "r") as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quoting=csv.QUOTE_ALL)
            for row in reader:
                entry = None
                if(len(row) == 0):
                    continue;

                desc = self.filter_desc(row[5])
                if(row[0].startswith("VISA")):
                    if(len(row[11]) > 0 and len(row[12]) == 0):
                        entry = (datetime.datetime.strptime(row[3], "%Y/%m/%d"), False, desc, decimal.Decimal(row[11]))
                    elif(len(row[11]) == 0 and len(row[12]) > 0):
                        entry = (datetime.datetime.strptime(row[3], "%Y/%m/%d"), False, desc, decimal.Decimal(-1)*decimal.Decimal(row[12]))
                    else:
                        raise RuntimeError("Col 11 and 12 for Visa have values!")
                else:
                    if(len(row[8]) > 0 and len(row[7]) == 0):
                        entry = (datetime.datetime.strptime(row[3], "%Y/%m/%d"), True, desc, decimal.Decimal(row[8]))
                    elif(len(row[8]) == 0 and len(row[7]) > 0):
                        entry = (datetime.datetime.strptime(row[3], "%Y/%m/%d"), True, desc, decimal.Decimal(-1.0) * decimal.Decimal(row[7]))
                    else:
                        raise RuntimeError("Col 8 and 7 for Credit have values!")
                
                if(entry):
                    self.entries.append(entry)
