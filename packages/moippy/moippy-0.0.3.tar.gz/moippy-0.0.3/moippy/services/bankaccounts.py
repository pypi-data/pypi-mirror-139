
from moippy.utils.moip import *
from moippy import BankAccount
from moippy.entities.lib.datatype import ListType

def BankAccounts(account_id:str):
    data = Get(f"/accounts/{account_id}/bankaccounts")
    return ListType(BankAccount).add([BankAccount(**item) for item in data["bankAccounts"]]) if "bankAccounts" in data and isinstance(data["bankAccounts"], list) else ListType(BankAccount)
