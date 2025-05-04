import csv
import datetime
import decimal
import re
import bankconverter.bank

# "Date","Description","BONIDOLLARS","Montant","Lien"
# "31 MAR31 Mars","RestaurantsChatime","2 %","9,28 $","31 Mars Chatime 9,28 $"


class AccesDCredit(bankconverter.bank.Bank):
    def __init__(self) -> None:
        super().__init__()

    def add(self, file: str) -> None:
        date_pattern = re.compile(r"^\d+ ([A-Za-z]+)(\d+).* ([0-9]+)$")
        with open(file, "r", encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
            for row in reader:
                if row['Date'] == "Total":
                    continue
                entry = bankconverter.bank.Transaction()

                date_str = row['Date']
                date_str = re.sub('D\u00C9C', 'dec', date_str)
                date_str = re.sub('nov.', 'nov', date_str)
                date_str = re.sub('sept.', 'sep', date_str)
                date_str = re.sub('AO\u00DB', 'AUG', date_str)
                date_str = re.sub('MAI', 'MAY', date_str)
                date_str = re.sub('AVR', 'apr', date_str)
                date_str = re.sub('F\u00C9V', 'FEB', date_str)
                match = date_pattern.match(date_str)
                if match:
                    date_str = "{} {} {}".format(match.group(2), match.group(1), match.group(3))

                entry.date = datetime.datetime.strptime(date_str, "%d %b %Y")

                entry.description = self.filter_desc(row['Description'])
                entry.account = None
                entry.credit = None

                if row['Montant']:
                    entry.credit = decimal.Decimal(re.sub(r'[^\d.\-]', '', re.sub(r',', '.', row['Montant'])))
                    if '+' in row['Montant']:
                        entry.credit *= -1

                    if entry.description == 'Paiement':
                        entry.account = entry.credit
                else:
                    raise RuntimeError("No match")

                self.entries.append(entry)
