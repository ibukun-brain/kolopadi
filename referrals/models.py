from decimal import Decimal

import auto_prefetch
from django.db import models
from django.db.models import Sum

from kolopadi.utils.models import TimeBasedModel


class Referral(TimeBasedModel):
    referrer = auto_prefetch.ForeignKey(
        "home.CustomUser",
        verbose_name="referrer",
        on_delete=models.CASCADE,
        related_name="referrer_referral",
        help_text="The user who referred new users",
    )
    referee = auto_prefetch.ForeignKey(
        "home.CustomUser",
        on_delete=models.CASCADE,
        related_name="referee_referral",
        help_text="New users being referred by the referrer",
    )
    ref_code = models.CharField(
        max_length=10, blank=True, help_text="Referral code of the referrer"
    )
    bonus = models.DecimalField(
        decimal_places=2,
        max_digits=11,
        default=Decimal(500.00),
    )

    def __str__(self):
        return f"{self.referrer} referred {self.referee}"


class ReferralWalletBalance(TimeBasedModel):
    referrer = auto_prefetch.OneToOneField(
        "home.CustomUser", on_delete=models.CASCADE, related_name="referrer_balance"
    )
    balance = models.DecimalField(
        decimal_places=2,
        max_digits=11,
        default=Decimal(0.00),
    )

    def __str__(self):
        return f"{self.referrer} referral balance"

    @property
    def total_wallet_balance(self):
        amount = Referral.objects.filter(referrer=self.referrer).aggregate(
            total_balance=Sum(("bonus"))
        )
        if amount["total_balance"] is None:
            return "{0:.2f}".format(0)
        return "{0:.2f}".format(amount["total_balance"])

    @property
    def total_referrals(self):
        return Referral.objects.filter(referrer=self.referrer).count()
