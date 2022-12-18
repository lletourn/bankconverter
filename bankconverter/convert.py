#!/bin/env python3
import accesd
import accesdcred
import datetime
import rbc

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter


def main(argv=None):  # IGNORE:C0111
    try:
        parser = ArgumentParser(description="BankConverter", formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument("-d", "--date", dest="start_date", help="start date [default: %(default)s]")
        parser.add_argument("-b", "--bank", dest="bank_type", help="bank type[default: %(default)s]")
        parser.add_argument("--files", help="files to folder(s) with source file(s) [default: %(default)s]", nargs='+')
        args = parser.parse_args()

        files = args.files
        start_date = datetime.datetime.strptime(args.start_date, "%Y-%m-%d")

        bank = None
        if(args.bank_type == "accesd"):
            bank = accesd.AccesD()
        if(args.bank_type == "accesdcred"):
            bank = accesdcred.AccesDCredit()
        elif(args.bank_type == "rbc"):
            bank = rbc.RBC()
        else:
            raise(RuntimeError("Unknown bank type"))

        for f in files:
            bank.add(f)

        bank.entries.sort(key=lambda entry: entry.date)

        current_date = start_date
        next_date = start_date
        a_week = datetime.timedelta(days=7)
        while(next_date < bank.entries[0].date):
            current_date = next_date
            next_date = next_date + a_week

        for entry in bank.entries:
            if entry.date < start_date:
                continue
            while entry.date >= next_date:
                current_date = next_date
                next_date = current_date + a_week
                print("\n{:%Y-%m-%d}".format(current_date))

            print("{:%Y-%m-%d}\t{:%Y-%m-%d}\t{}\t{}\t{}".format(current_date, entry.date, entry.description, str(entry.account or ''), str(entry.credit or '')))
        return 0
    except KeyboardInterrupt:
        return 0


if __name__ == "__main__":
    main()
