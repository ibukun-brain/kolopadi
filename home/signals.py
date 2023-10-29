import random
import threading

from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import post_save
from django.dispatch import receiver
from djoser.signals import user_registered

from home.helpers import get_user_geo_data
from home.tasks import create_user_wallet_after_signup_task

# from kolopadi.utils.background_thread import BackgroundThread
from kolopadi.utils.functions import get_user_ip_address
from referrals.models import ReferralWalletBalance
from wallets.models import Wallet

User = get_user_model()


@receiver(signal=user_registered)
def save_user_ip_address_after_sign_up(user, request, **kwargs):
    user = User.objects.get(email=user.email)
    user_ip_address = get_user_ip_address(request)
    user.ip_address = user_ip_address
    # geo_data = BackgroundTBackgroundThread(target=get_user_geo_data, args=(request,))
    # geo_data = threading.Thread(
    #         target=get_user_geo_data,
    #         args=["197.211.32.243"],
    #         # args=[user_ip_address],
    #         daemon=True
    #     )
    # geo_data.start()
    # geo_data.join()
    # print(geo_data)
    # geo_data = get_user_geo_data(user_ip_address)
    geo_data = get_user_geo_data("197.211.32.243")
    user.city = geo_data["city"]
    user.longitude = geo_data["longitude"]
    user.latitude = geo_data["latitude"]
    user.region = geo_data["region"]
    user.save()


@receiver(signal=user_logged_in)
def save_user_ip_address_after_login(sender, user, request, **kwargs):
    user = User.objects.get(email=user.email)
    user_ip_address = get_user_ip_address(request)
    user.ip_address = user_ip_address
    # geo_data = get_user_geo_data(user_ip_address)
    geo_data = get_user_geo_data("197.211.32.243")
    user.city = geo_data["city"]
    user.longitude = geo_data["longitude"]
    user.latitude = geo_data["latitude"]
    user.region = geo_data["region"]
    user.save()


@receiver(post_save, sender=User)
def create_referral_wallet(instance, created, **kwargs):
    if created:
        ReferralWalletBalance.objects.create(
            referrer=instance,
        )


@receiver(post_save, sender=User)
def generate_username(instance, created, **kwargs):
    if created:
        instance.username = f"{instance.first_name}{random.randint(0, 10000)}"
        instance.save()


@receiver(post_save, sender=User)
def create_user_wallet_after_signup(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(
            user=instance,
        )
        account_name = instance.get_full_name()
        email = instance.email
        # mobile_no = instance.mobile_no.as_e164
        mobile_no = instance.mobile_no
        thread = threading.Thread(
            target=create_user_wallet_after_signup_task,
            args=[account_name, email, mobile_no],
            daemon=True,
        )
        thread.start()
