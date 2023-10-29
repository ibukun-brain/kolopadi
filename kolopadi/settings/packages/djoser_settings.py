from django.conf import settings

User = settings.AUTH_USER_MODEL
DJOSER = {
    "USER_ID_FIELD": "uid",
    "LOGIN_FIELD": "email",
    "USER_CREATE_PASSWORD_RETYPE": True,
    "SET_PASSWORD_RETYPE": True,
    "PASSWORD_CHANGED_EMAIL_CONFIRMATION": True,
    # "SEND_ACTIVATION_EMAIL": True,
    # "SEND_CONFIRMATION_EMAIL": True,
    "ACTIVATION_URL": "activate/{uid}/{token}",
    "PASSWORD_RESET_CONFIRM_URL": "password/reset/{uid}/{token}",
    "PASSWORD_RESET_SHOW_EMAIL_NOT_FOUND": True,
    "PASSWORD_RESET_CONFIRM_RETYPE": True,
    "SERIALIZERS": {
        # if user_create_password is True then user_create_password_retype serializer will be used
        # instead or user_create_serializer
        "user_create_password_retype": "home.api.serializers.CustomUserCreatePasswordRetypeSerializer",
        "user": "home.api.serializers.CustomUserSerializer",
        "current_user": "home.api.serializers.CustomUserSerializer",
    },
}
