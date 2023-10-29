from datetime import datetime

from home.models import CustomUser
from wallets.models import Bank, Transaction, Wallet


def create_user_wallet(
    account_name, account_reference, bank, barter_id, account_number, email
):
    # user, _ = CustomUser.objects.get_or_create(email=email)
    user = CustomUser.objects.get(email=email)
    wallet = Wallet.objects.select_related("user").get(user=user)
    wallet.account_reference = account_reference
    wallet.account_name = account_name
    wallet.account_number = account_number
    wallet.bank = bank
    wallet.barter_id = barter_id
    wallet.save()


def update_user_wallet_balance(balance, email):
    user = CustomUser.objects.get(email=email)
    wallet = Wallet.objects.select_related("user").get(user=user)
    wallet.balance = balance
    wallet.save()


def create_user_wallet_transactions(transactions, email):
    wallet = Wallet.objects.select_related("user").get(user__email=email)
    for transaction in transactions:
        date = datetime.strptime(transaction["date"], "%Y-%m-%dT%H:%M:%S%z").date()
        _user_wallet_transaction, _ = Transaction.objects.get_or_create(
            wallet=wallet,
            type=transaction["type"],
            reference=transaction["reference"],
            balance_before=transaction["balance_before"],
            balance_after=transaction["balance_after"],
            amount=transaction["amount"],
            remarks=transaction["remarks"],
            date=date,
        )


def create_banks(banks):
    for bank in banks:
        _bank, _ = Bank.objects.get_or_create(
            name=bank["name"],
            bank_code=bank["code"],
        )
