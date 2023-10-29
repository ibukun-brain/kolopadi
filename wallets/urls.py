from django.urls import path

from wallets.api import views as wallets_views
from wallets.views import FlutterwaveWebhookView

app_name = "wallets"

urlpatterns = [
    path(route="banks/", view=wallets_views.BankListAPIView.as_view(), name="banks"),
    path(
        route="transfer/", view=wallets_views.TransferAPIView.as_view(), name="wallet"
    ),
    path(
        route="transactions/",
        view=wallets_views.TransactionListAPIView.as_view(),
        name="wallet",
    ),
    path(route="wallet/", view=wallets_views.WalletAPIView.as_view(), name="wallet"),
    # path(
    #     route="transaction/<uuid:uid>/",
    #     view=wallets_views.TransactionDetailAPIView.as_view(),
    #     name="wallet"
    # )
    path(route="flutterwavewebhook/", view=FlutterwaveWebhookView, name="webhook"),
]
