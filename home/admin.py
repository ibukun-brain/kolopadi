from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.utils.translation import gettext_lazy as _

from home.models import CustomUser, IdentityInformation

admin.site.site_header = "Kolopadi Administration"
admin.site.site_title = "Kolopadi"
admin.site.index_title = "Kolopadi"


@admin.register(CustomUser)
class UserAdmin(DefaultUserAdmin):
    model = CustomUser
    fieldsets = (
        (None, {"fields": ("password",)}),
        (_("Extra ID"), {"fields": ("uid",)}),
        (
            _("Personal info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "username",
                    "email",
                    "mobile_no",
                    "gender",
                    "address",
                    "date_of_birth",
                    "profile_pic",
                    "referral_code",
                )
            },
        ),
        (
            _("Geographic Information"),
            {
                "classes": ("collapse",),
                "fields": (
                    "ip_address",
                    "longitude",
                    "latitude",
                    "city",
                    "region",
                ),
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "last_name",
                    "date_of_birth",
                    "email",
                    "mobile_no",
                    "gender",
                    "password1",
                    "password2",
                    "referral_code",
                ),
            },
        ),
    )
    list_display = [
        "first_name",
        "last_name",
        "email",
        "is_staff",
        "date_joined",
        "last_login",
        "is_superuser",
        "is_staff",
    ]
    ordering = (
        "first_name",
        "last_name",
    )
    list_display_links = ["first_name", "email"]
    list_filter = ["date_joined", "gender"]
    readonly_fields = ["uid"]
    search_fields = ["first_name", "last_name", "email", "mobile_no", "referral_code"]


@admin.register(IdentityInformation)
class IdentityInformationAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "identity_type",
        "expiry_date",
        "id_number",
        "id_has_expired",
        "status",
        "is_verified",
    ]
    search_fields = [
        "identity_type",
        "id_number",
        "user__first_name",
        "user__last_name",
        "user__email",
    ]
    raw_id_fields = ["user"]
    list_select_related = ["user"]
    date_hierarchy = "created_at"
    list_filter = ["identity_type", "created_at", "status"]
