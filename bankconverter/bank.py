from dataclasses import dataclass
import datetime
import decimal
import re
from typing import List
from typing import Optional
import unicodedata


@dataclass(init=False)
class Transaction:
    date: datetime.datetime
    description: str
    account: Optional[decimal.Decimal]
    credit: Optional[decimal.Decimal]


class Bank:
    def __init__(self) -> None:
        self.entries: List[Transaction] = list()

    def remove_accents(self, input_str: str) -> str:
        nfkd_form = unicodedata.normalize('NFKD', input_str)
        return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

    def filter_desc(self, value: str) -> str:
        value = value.replace('SAINT-CONSTANQC', '')
        value = value.replace('STE CATHERINEQC', '')
        value = value.replace('LAVAL QC', '')
        value = value.replace('ST HYACINTHE QC', '')

        value = re.sub(r"MONTREAL *QC$", "", value, flags=re.IGNORECASE)
        value = re.sub(r"DELSON *QC$", "", value, flags=re.IGNORECASE)
        value = re.sub(r"ST-CONSTANT *QC$", "", value, flags=re.IGNORECASE)
        value = re.sub(r", ST-CONSTANT", "", value, flags=re.IGNORECASE)
        value = re.sub(r"SAINT-LAMBERT *QC$", "", value, flags=re.IGNORECASE)
        value = re.sub(r", SAINT LAMBERT", "", value, flags=re.IGNORECASE)
        value = re.sub(r"CANDIAC +QC$", "", value, flags=re.IGNORECASE)
        value = re.sub(r"EDMONTON +AB$", "", value, flags=re.IGNORECASE)
        value = re.sub(r"BROSSARD +QC$", "", value, flags=re.IGNORECASE)
        value = re.sub(r"LA *PRAIRIE +QC$", "", value, flags=re.IGNORECASE)
        value = re.sub(r", LA PRAIRIE", "", value, flags=re.IGNORECASE)
        value = re.sub(r", PRAIRIE", "", value, flags=re.IGNORECASE)
        value = re.sub(r", LAPRAIRIE", "", value, flags=re.IGNORECASE)
        value = re.sub(r", TORONTO", "", value, flags=re.IGNORECASE)
        value = re.sub(r", SABREVOIS", "", value, flags=re.IGNORECASE)
        value = re.sub(r", Henryville", "", value, flags=re.IGNORECASE)
        value = re.sub(r", MONTREAL", "", value, flags=re.IGNORECASE)
        value = re.sub(r", NEW WESTMINST", "", value, flags=re.IGNORECASE)
        value = re.sub(r", SAINT-HUBERT", "", value, flags=re.IGNORECASE)
        value = re.sub(r", SAINT HUBERT", "", value, flags=re.IGNORECASE)
        value = re.sub(r", ST HUBERT", "", value, flags=re.IGNORECASE)
        value = re.sub(r", QUEBEC", "", value, flags=re.IGNORECASE)
        value = re.sub(r", BROSSARD", "", value, flags=re.IGNORECASE)
        value = re.sub(r", SAINT-CONSTAN", "", value, flags=re.IGNORECASE)
        value = re.sub(r", Vancouver", "", value, flags=re.IGNORECASE)
        value = re.sub(r", SAINT-LAURENT", "", value, flags=re.IGNORECASE)
        value = re.sub(r", Candiac", "", value, flags=re.IGNORECASE)
        value = re.sub(r", LONGUEUIL", "", value, flags=re.IGNORECASE)
        value = re.sub(r", POINTE-CLAIRE", "", value, flags=re.IGNORECASE)
        value = re.sub(r", GREENFIELD PA", "", value, flags=re.IGNORECASE)
        value = re.sub(r", SCARBOROUGH", "", value, flags=re.IGNORECASE)
        value = re.sub(r", BLAINVILLE", "", value, flags=re.IGNORECASE)
        value = re.sub(r", OTTAWA", "", value, flags=re.IGNORECASE)
        value = re.sub(r", ST PHILIPPE", "", value, flags=re.IGNORECASE)
        value = re.sub(r", LONDON", "", value, flags=re.IGNORECASE)
        value = re.sub(r", GRANBY", "", value, flags=re.IGNORECASE)
        value = re.sub(r", LACHINE", "", value, flags=re.IGNORECASE)
        value = re.sub(r", ETOBICOKE", "", value, flags=re.IGNORECASE)
        value = re.sub(r", CALGARY", "", value, flags=re.IGNORECASE)
        value = re.sub(r", DELSON", "", value, flags=re.IGNORECASE)
        value = re.sub(r", BURNABY", "", value, flags=re.IGNORECASE)
        value = re.sub(r", Wakefield", "", value, flags=re.IGNORECASE)
        value = re.sub(r", BELOEIL", "", value, flags=re.IGNORECASE)
        value = re.sub(r", BOUCHERVILLE", "", value, flags=re.IGNORECASE)
        value = re.sub(r", SAINT-BLAISE-", "", value, flags=re.IGNORECASE)
        value = re.sub(r", MOUNT ROYAL S", "", value, flags=re.IGNORECASE)

        value = re.sub(r", g.co/helppay#", "", value, flags=re.IGNORECASE)

        value = re.sub(r", WWW.AMAZON.CA", "", value, flags=re.IGNORECASE)
        value = re.sub(r", AMAZON.CA", "", value, flags=re.IGNORECASE)

        if ',' in value:
            print(f"Comma found: {value}")

        return value.rstrip()
