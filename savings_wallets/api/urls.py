from django.urls import path

from savings_wallets.api.views import (
    SavingsCategoryAPIView,
    SavingsDetailAPIView,
    SavingsListAPIView,
    SavingsWithdrawalAPIView,
)

app_name = "savings_wallets"

urlpatterns = [
    path(
        route="savings/category/",
        view=SavingsCategoryAPIView.as_view(),
        name="savings-category",
    ),
    path(route="savings/", view=SavingsListAPIView.as_view(), name="savings"),
    path(
        route="savings/<uuid:uid>/",
        view=SavingsDetailAPIView.as_view(),
        name="savings-detail",
    ),
    path(
        route="savings/<uuid:uid>/withdraw/",
        view=SavingsWithdrawalAPIView.as_view(),
        name="savings-withdrawal",
    ),
]
