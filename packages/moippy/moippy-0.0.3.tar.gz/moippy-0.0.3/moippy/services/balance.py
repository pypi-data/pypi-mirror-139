
from moippy.utils.moip import *
from moippy import BankAccount
from moippy.entities.lib.datatype import ListType

def Balance():
    data = Get(f"/balances")
    for item in data:
        del item['_links']
    return data[0]
