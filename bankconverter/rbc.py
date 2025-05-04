import csv
import datetime
import decimal
import logging
import re
import bankconverter.bank


logger = logging.getLogger(__name__)


class RBC(bankconverter.bank.Bank):
    def __init__(self) -> None:
        super().__init__()

    def add(self, filename: str) -> None:
        with open(filename, "r", encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',', quoting=csv.QUOTE_ALL)
            for row in reader:
                if not row['Date']:
                    logger.warning("Empty row: %s", row)
                    continue

                entry = bankconverter.bank.Transaction()

                date_str = row['Date']
                # print(date_str)
                date_str = re.sub('d\u00E9c.', 'dec', date_str)
                date_str = re.sub('nov\\.', 'nov', date_str)
                date_str = re.sub('oct\\.', 'oct', date_str)
                date_str = re.sub('sept\\.', 'sep', date_str)
                date_str = re.sub('ao\u00FBt', 'aug', date_str)
                date_str = re.sub('juil', 'jul', date_str)
                date_str = re.sub('jul\\.', 'jul', date_str)
                date_str = re.sub('juin', 'jun', date_str)
                date_str = re.sub('mai', 'may', date_str)
                date_str = re.sub('avr.', 'apr', date_str)
                date_str = re.sub('mars', 'mar', date_str)
                date_str = re.sub('f\u00E9vr\\.', 'feb', date_str)
                date_str = re.sub('janv.', 'jan', date_str)
                # print(date_str)

                entry.date = datetime.datetime.strptime(date_str, "%d %b %Y")
                entry.description = self.filter_desc(row['Description'])
                entry.account = None
                entry.credit = None
                if 'Retraits' in row:
                    if row['Retraits']:
                        entry.account = decimal.Decimal(re.sub(r'[^\d.\-]', '', re.sub(r',', '.', row['Retraits'])))
                    else:
                        entry.account = decimal.Decimal(re.sub(r'[^\d.\-]', '', re.sub(r',', '.', row['D\u00E9p\u00F4ts'])))
                elif 'D\u00E9bit' in row:
                    if row['D\u00E9bit']:
                        entry.credit = decimal.Decimal(re.sub(r'[^\d.\-]', '', re.sub(r',', '.', row['D\u00E9bit'])))
                    else:
                        entry.credit = decimal.Decimal(re.sub(r'[^\d.\-]', '', re.sub(r',', '.', row['Cr\u00E9dit'])))
                else:
                    raise RuntimeError("Weird row: {}".format(row))

                self.entries.append(entry)
