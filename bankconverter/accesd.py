import csv
import datetime
import decimal
import re
import bankconverter.bank


class AccesD(bankconverter.bank.Bank):
    def __init__(self):
        super().__init__()

    def add(self, file):
        with open(file, "r", encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
            for row in reader:
                entry = bankconverter.bank.Transaction()

                date_str = row['Date']
                date_str = re.sub('D\u00C9C', 'dec', date_str)
                date_str = re.sub('nov.', 'nov', date_str)
                date_str = re.sub('sept.', 'sep', date_str)
                date_str = re.sub('AO\u00DB', 'aug', date_str)
                date_str = re.sub('MAI', 'may', date_str)
                date_str = re.sub('AVR', 'apr', date_str)
                date_str = re.sub('F\u00C9V', 'feb', date_str)
                entry.date = datetime.datetime.strptime(date_str, "%d %b %Y")
                entry.description = self.filter_desc(row['Descriptif'])
                entry.account = None
                entry.credit = None

                if row['Retrait ($)']:
                    entry.account = -1*decimal.Decimal(re.sub(r'[^\d.\-]', '', re.sub(r',', '.', row['Retrait ($)'])))
                elif row['Dépôt ($)']:
                    entry.account = decimal.Decimal(re.sub(r'[^\d.\-]', '', re.sub(r',', '.', row['Dépôt ($)'])))
                else:
                    raise RuntimeError("No match")

                self.entries.append(entry)
