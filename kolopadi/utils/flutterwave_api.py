import json

import requests

from kolopadi.utils.env_variable import get_env_variable


class WalletAPI:
    def __init__(self, secret_key=None, public_key=None):
        self.url = "https://api.flutterwave.com/v3"
        self.secret_key = get_env_variable("FLUTTERWAVE_SECRET_KEY", "XXX-XXX")
        self.public_key = get_env_variable("FLUTTERWAVE_PUBLIC_KEY", "XXX-XXX")

    def create_user_wallet(
        self, account_name, email, mobilenumber, country, bank_code=None
    ):
        """
        Creates Wallet for Users `bank_code` is not required but
        Expected values are 035 (Wema bank) and 232(Sterling bank).
        """
        url = self.url + "/payout-subaccounts/"
        headers = {
            "Authorization": f"Bearer {self.secret_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "account_name": account_name,
            "mobilenumber": mobilenumber,
            "email": email,
            "country": country,
            "bank_code": bank_code,
        }

        try:
            r = requests.post(
                url, data=json.dumps(payload), headers=headers, timeout=60
            )
        except Exception as e:
            raise e

        resp = json.loads(r.text)
        return resp

    def retrieve_user_virtual_account_number(self, account_reference):
        """
        Retrieves user virtual account number after successful
        wallet creation.
        """
        url = (
            self.url
            + f"/payout-subaccounts/{account_reference}/"
            + "static-account?currency=NGN"
        )

        headers = {
            "Authorization": f"Bearer {self.secret_key}",
            "Content-Type": "application/json",
        }

        try:
            r = requests.get(url, headers=headers, timeout=60)
        except Exception as e:
            raise e

        resp = json.loads(r.text)
        return resp

    def retrieve_wallet_balance(self, account_reference):
        url = self.url + f"/payout-subaccounts/{account_reference}/balances"
        headers = {
            "Authorization": f"Bearer {self.secret_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "currency": "NGN",
        }

        try:
            r = requests.get(url, data=json.dumps(payload), headers=headers, timeout=60)
        except Exception as e:
            raise e
        resp = json.loads(r.text)
        return resp

    def retrieve_wallet_transactions(self, account_reference, date_from="", date_to=""):
        url = self.url + f"/payout-subaccounts/{account_reference}/transactions"
        headers = {
            "Authorization": f"Bearer {self.secret_key}",
            "Content-Type": "application/json",
        }
        payload = {"from": date_from, "to": date_to, "currency": "NGN"}

        try:
            r = requests.get(url, data=json.dumps(payload), headers=headers, timeout=60)
        except Exception as e:
            raise e
        resp = json.loads(r.text)
        return resp

    def verify_user_transaction(self, id):
        url = self.url + f"/{id}/verify"

        headers = {
            "Authorization": f"Bearer {self.secret_key}",
            "Content-Type": "application/json",
        }

        try:
            r = requests.get(url, headers=headers, timeout=60)
        except Exception as e:
            raise e

        resp = json.loads(r.text)
        return resp

    def retrieve_banks(self):
        url = self.url + "/banks/NG"
        headers = {
            "Authorization": f"Bearer {self.secret_key}",
            "Content-Type": "application/json",
        }

        try:
            r = requests.get(url, headers=headers, timeout=60)
        except Exception as e:
            raise e
        resp = json.loads(r.text, strict=False)
        return resp

    def resolve_account_detail(self, account_number, account_bank):
        url = self.url + "/accounts/resolve"
        headers = {
            "Authorization": f"Bearer {self.secret_key}",
            "Content-Type": "application/json",
        }
        payload = {"account_number": account_number, "account_bank": account_bank}

        try:
            r = requests.post(
                url, data=json.dumps(payload), headers=headers, timeout=60
            )
        except Exception as e:
            raise e

        resp = json.loads(r.text, strict=False)
        return resp

    def initiate_transfer(
        self,
        account_bank,
        account_number,
        amount,
        narration,
        debit_subaccount,
    ):
        """
        Send money to another wallet or bank account
        """
        url = self.url + "/transfers"
        headers = {
            "Authorization": f"Bearer {self.secret_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "account_bank": account_bank,
            "account_number": account_number,
            "amount": amount,
            "currency": "NGN",
            "debit_currency": "NGN",
            "narration": narration,
            "debit_subaccount": debit_subaccount,
        }

        try:
            r = requests.post(
                url, data=json.dumps(payload), headers=headers, timeout=60
            )
        except Exception as e:
            raise e
        resp = json.loads(r.text, strict=False)
        return resp

    def get_transfer_rate(
        self,
        amount,
        destination_currency="NGN",
        source_currency="NGN",
    ):
        """
        Use this to get the transfer rate/fee which varies based on amount
        """
        url = (
            self.url
            + f"/transfers/rates?amount={amount}"
            + f"&destination_currency={destination_currency}"
            + f"&source_currency={source_currency}"
        )
        headers = {
            "Authorization": f"Bearer {self.secret_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "amount": amount,
            "source_currency": source_currency,
            "destination_currency": destination_currency,
        }
        print(payload)

        try:
            r = requests.get(url, data=json.dumps(payload), headers=headers, timeout=60)
        except Exception as e:
            raise e
        resp = json.loads(r.text, strict=False)
        return resp

    def debit_user(self, transaction_id, phone_number, amount):
        """
        Use this to perform a debit on a sub wallet and credit the main wallet
        transaction_id: a unique transaction id to be generated by developer
        """

        url = self.sandbox + "/wallet/debit"
        headers = {
            "Authorization": "Bearer " + self.public_key,
            "Content-Type": "application/json",
        }
        payload = {
            "transactionReference": transaction_id,
            "amount": amount,
            "phoneNumber": phone_number,
            "secretKey": self.secret_key,
        }

        try:
            r = requests.post(
                url, data=json.dumps(payload), headers=headers, timeout=60
            )
        except Exception as e:
            raise e
        resp = json.loads(r.text, strict=False)
        return resp
