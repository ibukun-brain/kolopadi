import logging
import threading

from drf_spectacular.utils import extend_schema
from rest_framework import filters, generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from home.api.custom_permissions import IsWalletOwnerOrReadOnly
from home.tasks import user_wallet_transactions_task
from wallets.api.serializers import (
    BankSerializer,
    TransferSerializer,
    UserWalletSerializer,
    WalletTransactionSerializer,
)
from wallets.models import Bank, Transaction, Wallet
from wallets.tasks import bank_task

logger = logging.getLogger(__name__)


class BankListAPIView(generics.ListAPIView):
    serializer_class = BankSerializer
    queryset = Bank.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "bank_code"]

    def get(self, request, *args, **kwargs):
        thread = threading.Thread(target=bank_task, daemon=True)
        thread.start()
        return self.list(request, *args, **kwargs)


class WalletAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserWalletSerializer
    permission_classes = [permissions.IsAuthenticated, IsWalletOwnerOrReadOnly]

    def get_queryset(self):
        qs = Wallet.objects.select_related("user").all()
        return qs

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
    permission_classes = [permissions.IsAuthenticated, IsWalletOwnerOrReadOnly]

    @extend_schema(parameters=[TransferSerializer])
    def post(self, request, format=None):
        print(request.data)
        serializer = TransferSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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