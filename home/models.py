import uuid

import auto_prefetch
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils import timezone
from django_resized import ResizedImageField

from kolopadi.utils.choices import Gender, IdentityType, Status
from kolopadi.utils.managers import CustomUserManager
from kolopadi.utils.media import MediaHelper
from kolopadi.utils.models import TimeBasedModel
from kolopadi.utils.strings import generate_ref_no
from kolopadi.utils.validators import FileValidatorHelper

# from phonenumber_field.modelfields import PhoneNumberField


class CustomUser(TimeBasedModel, AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    # REQUIRED_FIELDS = ["first_name", "last_name", "mobile_no", "referral_code"]

    username = models.CharField(max_length=50, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    uid = models.UUIDField(default=uuid.uuid4)
    email = models.EmailField(verbose_name="email address", unique=True)
    mobile_no = models.CharField(
        max_length=11,
        unique=True,
        error_messages={
            "unique": ("A user with that Mobile Number already exists."),
        },
        validators=[MinLengthValidator(11)],
    )
    referral_code = models.CharField(max_length=10, blank=True, unique=True)
    date_joined = models.DateTimeField(default=timezone.now)
    date_of_birth = models.DateField(null=True)
    address = models.CharField(max_length=40, blank=True)
    gender = models.CharField(max_length=15, choices=Gender.choices)
    profile_pic = ResizedImageField(
        upload_to=MediaHelper.get_image_upload_path,
        blank=True,
        verbose_name="Profile Picture",
        validators=[
            FileValidatorHelper.validate_file_size,
            FileValidatorHelper.validate_image_extension,
        ],
    )
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True
    )
    city = models.CharField(max_length=50, blank=True)
    region = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects = CustomUserManager()

    class Meta(auto_prefetch.Model.Meta):
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["date_joined"]
        indexes = [models.Index(fields=["date_joined"])]

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    @property
    def image_url(self):

        if self.profile_pic:
            return self.profile_pic.url

        return f"http://localhost:8000{settings.STATIC_URL}avatar/placeholder.jpg"

    def __str__(self):
        return self.get_full_name() or self.email

    def save(self, *args, **kwargs):

        if not self.referral_code:
            self.referral_code = generate_ref_no(10)
        return super().save(*args, **kwargs)


class IdentityInformation(TimeBasedModel):
    user = models.OneToOneField("home.CustomUser", on_delete=models.CASCADE)
    identity_type = models.CharField(
        max_length=50, choices=IdentityType.choices, default=IdentityType.NIN
    )
    expiry_date = models.DateField(
        blank=True,
        null=True,
    )
    id_number = models.CharField(max_length=20, verbose_name="ID number")
    id_document = models.ImageField(
        upload_to=MediaHelper.get_image_upload_path,
        verbose_name="ID document",
        validators=[
            FileValidatorHelper.validate_file_size,
            FileValidatorHelper.validate_image_extension,
        ],
    )
    status = models.CharField(
        max_length=50, choices=Status.choices, default=Status.Pending
    )
    feedback = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user} identity information"

    def id_has_expired(self):
        if self.expiry_date:
            return timezone.now().date() > self.expiry_date
        return False

    id_has_expired.boolean = True

    def is_verified(self):
        return self.status == "Verified"

    is_verified.boolean = True
