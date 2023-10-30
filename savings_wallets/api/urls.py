from django.urls import path

from savings_wallets.api.views import SavingsAPIView, SavingsCategoryAPIView

app_name = "savings_wallets"

urlpatterns = [
    path(
        route="savings/category/",
        view=SavingsCategoryAPIView.as_view(),
        name="savings-category",
    ),
    path(route="savings/", view=SavingsAPIView.as_view(), name="savings"),
]
