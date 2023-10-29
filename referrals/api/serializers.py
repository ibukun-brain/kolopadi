from rest_framework import serializers

from referrals.models import ReferralWalletBalance


class UserReferralWalletSerializer(serializers.ModelSerializer):
    referrer = serializers.StringRelatedField()

    class Meta:
        model = ReferralWalletBalance
        fields = ["referrer", "balance", "total_wallet_balance", "total_referrals"]
