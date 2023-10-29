from django.contrib import admin

from savings_wallets.models import Savings, SavingsCategory


@admin.register(SavingsCategory)
class SavingsCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    search_fields = ["name"]


@admin.register(Savings)
class SavingsAdmin(admin.ModelAdmin):
    list_display = [
        "category",
        "name",
        "amount",
        "target",
        "frequency",
        "saving_type",
        "start_date",
        "end_date",
    ]
    list_display_links = ["name"]
    raw_id_fields = ["category"]
    list_select_related = ["category"]
    search_fields = ["name"]
    list_filter = [
        ("category", admin.RelatedOnlyFieldListFilter),
        "frequency",
        "saving_type",
    ]
    date_hierarchy = "start_date"
