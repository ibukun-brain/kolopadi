import threading

from django.contrib.auth import get_user_model
from django_user_agents.utils import get_user_agent
from djoser.serializers import UserCreatePasswordRetypeSerializer, UserSerializer
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from home.models import CustomUser
from home.tasks import send_email_task
from referrals.models import Referral

User = get_user_model()


class CustomUserCreatePasswordRetypeSerializer(UserCreatePasswordRetypeSerializer):
    referral_code = serializers.CharField(max_length=50, allow_blank=True)

    class Meta(UserCreatePasswordRetypeSerializer.Meta):
        model = User
        fields = [
            "first_name",
            "last_name",
            "date_of_birth",
            "email",
            "mobile_no",
            "gender",
            "password",
            "referral_code",
        ]

    def create(self, validated_data):
        # request = self.context.get("request")
        referral_code = validated_data.pop("referral_code")
        new_user = super().create(validated_data)
        thread = threading.Thread(
            target=send_email_task,
            args=[new_user.get_full_name(), validated_data.get("email")],
            daemon=True,
        )
        thread.start()
        referrer = None
        if not referral_code or referral_code != "":
            try:
                referrer = CustomUser.objects.get(referral_code=referral_code)
            except CustomUser.DoesNotExist:
                pass

            if referrer:
                Referral.objects.create(
                    referrer=referrer, referee=new_user, ref_code=referral_code
                )
        return new_user


class CustomUserSerializer(UserSerializer):
    """
    Using django user agent package we can get the user device
    and serialize the data
    """

    user_device = serializers.SerializerMethodField(method_name="get_user_device")

    @extend_schema_field(OpenApiTypes.STR)
    def get_user_device(self, obj):
        request = self.context.get("request")
        user_agent = get_user_agent(request)
        return user_agent.os.family

    class Meta(UserSerializer.Meta):
        model = CustomUser
        fields = (
            "first_name",
            "last_name",
            "username",
            "profile_pic",
            "image_url",
            "email",
            "mobile_no",
            "ip_address",
            "latitude",
            "longitude",
            "city",
            "region",
            "user_device",
        )
        extra_kwargs = {
            "first_name": {
                "read_only": True,
            },
            "last_name": {
                "read_only": True,
            },
            "email": {
                "read_only": True,
            },
            "mobile_no": {
                "read_only": True,
            },
            "latitude": {
                "read_only": True,
            },
            "longitude": {
                "read_only": True,
            },
            "city": {
                "read_only": True,
            },
            "region": {
                "read_only": True,
            },
            "ip_address": {
                "read_only": True,
            },
        }


# class UserAddressBookSerializer(serializers.ModelSerializer):
#     user = CustomUserCreateSerializer()

#     class Meta:
#         model = AddressBook
#         fields = (
#             'user', 'phone_no', 'additional_phone_no',
#             'delivery_address', 'default_address',
#             'state', 'city', 'town'
#         )
