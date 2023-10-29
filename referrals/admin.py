from django.contrib import admin

from referrals.models import Referral, ReferralWalletBalance


@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ["referrer", "ref_code", "created_at"]
    list_select_related = ["referrer", "referee"]
    search_fields = [
        "referrer__first_name",
        "referrer__last_name",
        "referrer__email",
        "referee__first_name",
        "referrer__last_name",
        "referee__email",
        "ref_code",
    ]
    # readonly_fields = ['referrer', 'referee']
    raw_id_fields = ["referrer", "referee"]
    date_hierarchy_fields = "created_at"
    list_filter = ["created_at"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related("referrer", "referee")
        return qs


@admin.register(ReferralWalletBalance)
class ReferralWalletBalanceAdmin(admin.ModelAdmin):
    list_display = ["referrer", "balance"]
    list_select_related = ["referrer"]
    raw_id_fields = ["referrer"]
    date_hierarchy_fields = "created_at"
    list_filter = ["created_at"]
    search_fields = ["referrer__email", "referrer_first_name", "referrer_last_name"]
