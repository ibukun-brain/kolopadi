from requests.exceptions import RequestException

from home.flutterwave_utils import create_banks
from kolopadi.utils.flutterwave_api import WalletAPI

wallet_api = WalletAPI()


def bank_task():
    get_banks = wallet_api.retrieve_banks()
    if get_banks["status"] == "error":
        raise RequestException()
    banks = get_banks["data"]
    return create_banks(banks=banks)


def initiate_transfer_task(
    account_bank, account_number, amount, narration, debit_subaccount
):
    transfer = wallet_api.initiate_transfer(
        account_bank, account_number, amount, narration, debit_subaccount
    )
    print(transfer)
    return transfer
