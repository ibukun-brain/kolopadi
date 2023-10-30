from django.conf import settings
from django.core.mail import send_mail
from requests.exceptions import RequestException

from home.flutterwave_utils import (
    create_user_wallet,
    create_user_wallet_transactions,
    update_user_wallet_balance,
)
from kolopadi.utils.flutterwave_api import WalletAPI

# from kolopadi.utils.vtpass_api import VtPassAPI

wallet_api = WalletAPI()


# def send_otp_task(self, sender, responsetype, recipient, message):
#     """Run background task to send otp"""
#     vtpass_api = VtPassAPI()
#     otp_sms = vtpass_api.send_sms(
#         sender=sender, responsetype=responsetype, recipient=recipient, message=message
#     )
#     if otp_sms["messages"][0]["statusCode"] == "2222":
#         raise RequestException()


def create_user_wallet_after_signup_task(
    account_name,
    email,
    mobile_no,
):
    """Run background task to create a new wallet"""
    # this doesn't help i can just stick with using wema bank code
    # but what if wema bank code also goes down
    # bank_code = random.choice(["232", "035"])
    new_user_wallet = wallet_api.create_user_wallet(
        account_name=account_name,
        email=email,
        mobilenumber=mobile_no,
        country="NG",
        bank_code="232",
    )
    print(new_user_wallet)
    if new_user_wallet["status"] == "error":
        raise RequestException()
    account_reference = new_user_wallet["data"]["account_reference"]
    account_name = new_user_wallet["data"]["account_name"]
    account_number = new_user_wallet["data"]["nuban"]
    bank = new_user_wallet["data"]["bank_name"]
    barter_id = new_user_wallet["data"]["barter_id"]

    return create_user_wallet(
        account_name=account_name,
        account_reference=account_reference,
        bank=bank,
        barter_id=barter_id,
        email=email,
        account_number=account_number,
    )


def user_wallet_balance_task(email, account_reference):
    """Run background task to fetch user wallet balance"""
    retrieve_wallet_balance = wallet_api.retrieve_wallet_balance(
        account_reference=account_reference
    )
    # print(retrieve_wallet_balance)
    if retrieve_wallet_balance["status"] == "error":
        raise RequestException()

    balance = retrieve_wallet_balance["data"]["available_balance"]
    return update_user_wallet_balance(balance=balance, email=email)


def user_wallet_transactions_task(
    email,
    account_reference,
):
    retrieve_wallet_transactions = wallet_api.retrieve_wallet_transactions(
        account_reference=account_reference,
    )
    # print(retrieve_wallet_transactions)
    if retrieve_wallet_transactions["status"] == "error":
        raise RequestException()
    transactions = retrieve_wallet_transactions["data"]["transactions"]
    return create_user_wallet_transactions(
        transactions=transactions,
        email=email,
    )


def send_email_task(url, user, email):
    send_mail(
        subject="Welcome to Kolopadi",
        message=f"Hello {user}\n"
        + "Thank you for choosing Kolopadi!\n"
        + "Login into www.stakefair.io and discover "
        + "the fantastic promotions that await you!\n",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
    )
