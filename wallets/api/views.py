import logging
import threading
from decimal import Decimal

from drf_spectacular.utils import extend_schema
from rest_framework import filters, generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from home.api.custom_permissions import IsWalletOwnerOrReadOnly
from home.tasks import user_wallet_balance_task, user_wallet_transactions_task
from kolopadi.utils.flutterwave_api import WalletAPI
from wallets.api.serializers import (
    BankAccountDetailSerializer,
    BankSerializer,
    TransferSerializer,
    UserWalletSerializer,
    WalletTransactionSerializer,
)
from wallets.models import Bank, Transaction, Wallet
from wallets.tasks import bank_task

logger = logging.getLogger(__name__)

wallet_api = WalletAPI()


class BankListAPIView(generics.ListAPIView):
    serializer_class = BankSerializer
    queryset = Bank.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "bank_code"]

    def get(self, request, *args, **kwargs):
        thread = threading.Thread(target=bank_task, daemon=True)
        thread.start()
        return self.list(request, *args, **kwargs)


class ResolveBankAccountDetails(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        request=BankAccountDetailSerializer,
        responses=BankAccountDetailSerializer,
    )
    def post(self, request, *args, **kwargs):
        """
        Endpoint for resolving bank account details for transfer\n
        bank_code: The bank code from Banks endpoint\n
        account_number: The account number of the recipient\n
        """
        serializer = BankAccountDetailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            bank_code = serializer.data.get("bank_code")
            account_number = serializer.data.get("account_number")
            response = wallet_api.resolve_account_detail(account_number, bank_code)
            if response["status"] == "success":
                return Response(response, status=status.HTTP_201_CREATED)

        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class WalletAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserWalletSerializer
    permission_classes = [permissions.IsAuthenticated, IsWalletOwnerOrReadOnly]

    def get_queryset(self):
        qs = Wallet.objects.select_related("user").all()
        return qs

    def get(self, request, *args, **kwargs):
        user = request.user
        user_wallet = user.wallet
        thread = threading.Thread(
            target=user_wallet_balance_task,
            args=[user.email, user_wallet.account_reference],
            daemon=True,
        )
        thread.start()
        return self.retrieve(request, *args, **kwargs)

    def get_object(self):
        user = self.request.user
        wallet = user.wallet
        return wallet

    def perform_update(self, serializer):
        serializer.save(wallet=self.request.user.wallet)


class TransactionListAPIView(generics.ListAPIView):
    serializer_class = WalletTransactionSerializer
    permission_classes = [permissions.IsAuthenticated, IsWalletOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        user_wallet = user.wallet
        qs = Transaction.objects.select_related("wallet").filter(wallet=user_wallet)
        return qs

    def get(self, request, *args, **kwargs):
        user = self.request.user
        user_wallet = user.wallet
        thread = threading.Thread(
            target=user_wallet_transactions_task,
            args=[user.email, user_wallet.account_reference],
            daemon=True,
        )
        thread.start()
        return self.list(request, *args, **kwargs)


class TransferAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        request=TransferSerializer,
        responses=TransferSerializer,
    )
    def post(self, request, format=None):
        user = self.request.user
        user_wallet = user.wallet
        serializer = TransferSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            account_bank = serializer.data.get("bank_code")
            account_number = serializer.data.get("account_number")
            print(account_number)
            amount = serializer.data.get("amount")
            narration = serializer.data.get("narration", "no narration")
            response = wallet_api.initiate_transfer(
                account_bank,
                account_number,
                amount,
                narration,
                user_wallet.account_reference,
            )
            print(response)
            if response["status"] == "error":
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            fee = response.get("data")["fee"]
            total_charge = float(amount) + fee
            if Decimal(total_charge) <= user_wallet.balance:
                data = {
                    "amount": amount,
                    "error": "false",
                    "message": "Successful",
                }
                # thread = threading.Thread(
                #     target=initiate_transfer_task,
                #     args=[
                #         account_bank,
                #         account_number,
                #         amount,
                #         narration,
                #         user_wallet.account_reference
                #     ],
                #     daemon=True,
                # )
                # thread.start()
                #             response = AsyncResult(initiate_transfer.id)
                #             fee = response.get().get("data")["fee"]
                #             amount = account_details["amount"]
                #             self.request.session["total_charge"] = fee + float(amount)
                serializer.save()
                return Response(data, status=status.HTTP_201_CREATED)
            data = {
                "amount": amount,
                "error": "true",
                "message": "Insufficient funds",
            }
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

        # bank = Bank.objects.get(bank_code=transaction_details["bank_code"])
        # beneficiary, _ = Beneficiary.objects.get_or_create(
        #     wallet=request.user.wallet,
        #     bank=bank,
        #     account_name=transaction_details["account_name"],
        #     account_number=transaction_details["account_number"],
        # )
        # if add_to_beneficiary == "True":
        #     beneficiary.is_favourite = True
        # beneficiary.save()


# user = self.request.user
#             user_wallet = user.wallet
#             initiate_transfer = initiate_transfer_task.delay(
#                 account_bank=account_details["bank_code"],
#                 account_number=account_details["account_number"],
#                 amount=account_details["amount"],
#                 narration=account_details["narration"],
#                 debit_subaccount=user_wallet.account_reference,
#             )
#             response = AsyncResult(initiate_transfer.id)
#             fee = response.get().get("data")["fee"]
#             amount = account_details["amount"]
#             self.request.session["total_charge"] = fee + float(amount)
