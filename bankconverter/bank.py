from dataclasses import dataclass
import datetime
import decimal
import re
import unicodedata


@dataclass(init=False)
class Transaction:
    date: datetime
    description: str
    account: decimal.Decimal
    credit: decimal.Decimal


class Bank(object):
    def __init__(self):
        self.entries = list()

    def remove_accents(self, input_str):
        nfkd_form = unicodedata.normalize('NFKD', input_str)
        return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

    def filter_desc(self, value):
        value = value.replace('SAINT-CONSTANQC', '')
        value = value.replace('STE CATHERINEQC', '')
        value = value.replace('LAVAL QC', '')
        value = value.replace('ST HYACINTHE QC', '')

        value = re.sub(r"MONTREAL *QC$", "", value)
        value = re.sub(r"DELSON *QC$", "", value)
        value = re.sub(r"ST-CONSTANT *QC$", "", value)
        value = re.sub(r"SAINT-LAMBERT *QC$", "", value)
        value = re.sub(r"CANDIAC +QC$", "", value)
        value = re.sub(r"EDMONTON +AB$", "", value)
        value = re.sub(r"BROSSARD +QC$", "", value)
        value = re.sub(r"LA *PRAIRIE +QC$", "", value)

        return value.rstrip()
