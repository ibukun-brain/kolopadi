from decimal import Decimal

from django.contrib import admin, messages
from django.utils.translation import ngettext

from wallets.models import Bank, SecurityQuestion, Transaction, Wallet, WalletSecurity


@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ["name", "bank_code"]
    search_fields = ["name"]
    ordering = ["name"]
    list_per_page = 50


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ["user", "account_number", "balance"]
    raw_id_fields = ["user"]
    list_select_related = ["user"]
    ordering = ["balance"]
    readonly_fields = ["uid"]
    search_fields = ["user__email", "user__first_name", "account_number", "bank"]


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = [
        "wallet",
        "type",
        "date",
        "balance_before",
        "balance_after",
        # "amount",
        "amount_in_naira",
    ]
    list_filter = ["type", "date"]
    list_search_fields = [
        "wallet__email",
        "wallet__first_name",
        "wallet__last_name",
        "wallet__mobile_no",
        "remarks",
        "reference",
    ]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "wallet",
                    "type",
                    "date",
                    "balance_before",
                    "balance_after",
                    "amount",
                )
            },
        ),
        (
            ("Bill Transaction"),
            {
                "classes": ("collapse",),
                "fields": (
                    "bill_service",
                    "vt_pass_request_id",
                    "vtpass_transaction_id",
                    "phone_number",
                ),
            },
        ),
        (
            ("Transfer Transaction"),
            {
                "classes": ("collapse",),
                "fields": (
                    "transfer_status",
                    "external_recipient",
                    "external_recipient_account_no",
                    "external_recipient_bank",
                    "recipient_wallet",
                ),
            },
        ),
    )
    raw_id_fields = [
        "wallet",
        # "bill_service",
        "recipient_wallet",
    ]
    readonly_fields = ["uid"]
    date_hierarchy = "date"
    list_per_page = 50

    def amount_in_naira(self, obj):
        return "₦{0:.2f}".format(Decimal(obj.amount))

    amount_in_naira.short_description = "amount"


@admin.register(SecurityQuestion)
class SecurityQuestionAdmin(admin.ModelAdmin):
    list_display = ["question", "visible"]
    readonly_fields = ["uid"]
    search_fields = ["question"]
    list_filter = ["created_at", "updated_at", "visible"]
    date_hierarchy = "created_at"
    actions = ["make_visible", "make_not_visible"]

    @admin.action(description="Mark selected questions as not visible")
    def make_not_visible(self, request, queryset):
        updated = queryset.update(visible=False)
        self.message_user(
            request,
            ngettext(
                "%d question was successfully marked as not visible.",
                "%d questions were successfully marked as not visible.",
                updated,
            )
            % updated,
            messages.SUCCESS,
        )

    @admin.action(description="Mark selected questions as visible")
    def make_visible(self, request, queryset):
        updated = queryset.update(visible=True)
        self.message_user(
            request,
            ngettext(
                "%d question was successfully marked as visible.",
                "%d questions were successfully marked as visible.",
                updated,
            )
            % updated,
            messages.SUCCESS,
        )


@admin.register(WalletSecurity)
class WalletSecurityAdmin(admin.ModelAdmin):
    list_display = ["wallet", "security_question"]
    readonly_fields = ["uid", "answer"]
    date_hierarchy = "created_at"
    search_fields = ["wallet", "security_question"]
    list_filter = ["created_at", "updated_at"]
    raw_id_fields = ["wallet", "security_question"]
    list_select_related = ["wallet", "wallet__user", "security_question"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related("security_question", "wallet__user")
        return qs
