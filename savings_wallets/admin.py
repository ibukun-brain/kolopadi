from django.contrib import admin

from savings_wallets.models import Savings, SavingsCategory, SavingsWallet


@admin.register(SavingsCategory)
class SavingsCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    search_fields = ["name"]


@admin.register(Savings)
class SavingsAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "category",
        "name",
        "frequency_amount",
        "amount_to_save",
        "frequency",
        "type_of_savings",
        "start_date",
        "end_date",
    ]
    readonly_fields = ["uid"]
    list_display_links = ["user", "name"]
    raw_id_fields = ["category", "user"]
    list_select_related = ["category", "user"]
    search_fields = ["name"]
    list_filter = [
        ("category", admin.RelatedOnlyFieldListFilter),
        "frequency",
        "type_of_savings",
    ]
    date_hierarchy = "start_date"


@admin.register(SavingsWallet)
class SavingsWalletAdmin(admin.ModelAdmin):
    list_display = ["user", "balance"]
    raw_id_fields = ["user"]
    list_select_related = ["user"]
