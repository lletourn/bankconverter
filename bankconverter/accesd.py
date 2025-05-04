import csv
import datetime
import decimal
import bankconverter.bank


class AccesD(bankconverter.bank.Bank):
    def __init__(self) -> None:
        super().__init__()

    def add(self, file: str) -> None:
        # with open(file, "r", encoding='utf-8-sig') as csvfile:
        with open(file, "r", encoding='iso-8859-1') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in reader:
                if len(row) < 1:
                    continue
                entry = bankconverter.bank.Transaction()

                entry.date = datetime.datetime.strptime(row[3], "%Y/%m/%d")
                entry.description = self.filter_desc(row[5])
                entry.account = None
                entry.credit = None

                if not row[8] and not row[7]:
                    raise RuntimeError(f"Both not empty? {row[7]} vs {row[8]}")

                if row[8]:
                    entry.account = decimal.Decimal(row[8])
                elif row[7]:
                    entry.account = -1 * decimal.Decimal(row[7])
                else:
                    raise RuntimeError("No transactions")

                self.entries.append(entry)
