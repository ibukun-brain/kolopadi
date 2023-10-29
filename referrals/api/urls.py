from django.urls import path

from referrals.api.views import ReferralAPIView

app_name = "referrals"

urlpatterns = [
    path(route="referrals/", view=ReferralAPIView.as_view(), name="referral")
]
