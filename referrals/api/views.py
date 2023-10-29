from rest_framework import generics, permissions

from home.api.custom_permissions import IsReferrerOrReadOnly
from referrals.api.serializers import UserReferralWalletSerializer
from referrals.models import Referral


class ReferralAPIView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, IsReferrerOrReadOnly]
    serializer_class = UserReferralWalletSerializer
    queryset = Referral.objects.all()

    def get_object(self):
        user = self.request.user
        return user.referrer_balance
