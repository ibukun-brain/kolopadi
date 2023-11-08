from django.contrib import admin

from loans.models import Borrower, BorrowerWallet, Lender, LenderWallet, LoanListing


@admin.register(Borrower)
class BorrowerAdmin(admin.ModelAdmin):
    list_display = ["user", "verified"]
    list_select_related = ["user"]


@admin.register(BorrowerWallet)
class BorrowerWalletAdmin(admin.ModelAdmin):
    list_select_related = ["lender"]


@admin.register(Lender)
class LenderAdmin(admin.ModelAdmin):
    list_display = ["user", "verified"]
    list_select_related = ["user"]


@admin.register(LenderWallet)
class LenderWalletAdmin(admin.ModelAdmin):
    list_select_related = ["lender"]


@admin.register(LoanListing)
class LoanListingAdmin(admin.ModelAdmin):
    pass
