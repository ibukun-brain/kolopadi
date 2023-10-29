from decimal import Decimal

from django.db.models.signals import post_save
from django.dispatch import receiver

from referrals.models import Referral, ReferralWalletBalance


@receiver(post_save, sender=Referral)
def update_referral_balance(instance, created, *args, **kwargs):
    if created:
        referral_wallet_balance = ReferralWalletBalance.objects.get(
            referrer=instance.referrer
        )
        referral_wallet_balance.balance += Decimal(instance.bonus)
        referral_wallet_balance.save()
