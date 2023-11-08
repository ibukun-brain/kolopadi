import uuid

import auto_prefetch
from django.core.validators import MaxValueValidator
from django.db import models

from kolopadi.utils.models import TimeBasedModel


class Borrower(TimeBasedModel):
    user = auto_prefetch.OneToOneField("home.CustomUser", on_delete=models.CASCADE)
    username = models.CharField(max_length=50)
    bio = models.TextField(max_length=100, blank=True)
    verified = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=50)
    employement_type = models.CharField(max_length=50)
    profession_type = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.username}"


class BorrowerWallet(TimeBasedModel):
    borrower = auto_prefetch.OneToOneField(Borrower, on_delete=models.CASCADE)
    balance = models.DecimalField(
        max_digits=11,
        decimal_places=2,
        default=0.00,
    )

    def __str__(self):
        return f"{self.borrower}"


class BorrowerAsset(TimeBasedModel):
    uid = models.UUIDField(default=uuid.uuid4)
    loan_listing = auto_prefetch.ForeignKey("LoanListing", on_delete=models.CASCADE)
    asset_type = models.CharField(max_length=50)
    asset_value = models.DecimalField(max_digits=11, decimal_places=2)
    ownership_percentage = models.PositiveSmallIntegerField(
        default=0,
        validators=[MaxValueValidator(100)],
    )
    possession_since = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.uid


class BorrowerLiablity(TimeBasedModel):
    uid = models.UUIDField(default=uuid.uuid4)
    loan_listing = auto_prefetch.ForeignKey("LoanListing", on_delete=models.CASCADE)
    liability_cost = models.DecimalField(max_digits=11, decimal_places=2)
    liabliity_state_date = models.DateTimeField(auto_now_add=True)
    liabliity_end_date = models.DateTimeField(null=True)

    def __str__(self):
        return self.uid


class Lender(TimeBasedModel):
    user = auto_prefetch.OneToOneField(
        "home.CustomUser",
        on_delete=models.CASCADE,
    )
    username = models.CharField(max_length=50)
    bio = models.TextField(max_length=100, blank=True)
    verified = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.username}"


class LenderWallet(TimeBasedModel):
    lender = auto_prefetch.OneToOneField(Lender, on_delete=models.CASCADE)
    balance = models.DecimalField(
        max_digits=11,
        decimal_places=2,
        default=0.00,
    )

    def __str__(self):
        return f"{self.lender} lender wallet"


class LoanListing(TimeBasedModel):
    uid = models.UUIDField(default=uuid.uuid4)
    borrower = auto_prefetch.ForeignKey(Borrower, on_delete=models.CASCADE)
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    loan_tenure_in_months = models.PositiveIntegerField(default=1)
    reason_for_loan = models.TextField()
    title = models.CharField(max_length=100)
    ability_to_repay = models.TextField()

    def __str__(self):
        return f"{self.uid}"


class LenderProposal(TimeBasedModel):
    uid = models.UUIDField(default=uuid.uuid4)
    lender = auto_prefetch.ForeignKey(
        Lender, on_delete=models.CASCADE, related_name="lender_proposal"
    )
    loan_listing = auto_prefetch.ForeignKey(
        LoanListing, on_delete=models.CASCADE, related_name="lender_proposal"
    )
    cancel_date = models.DateTimeField(
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.lender} proposal"


class LoanListingFulfillment(TimeBasedModel):
    lender_proposal = auto_prefetch.ForeignKey(
        LenderProposal,
        on_delete=models.CASCADE,
        related_name="loan_listing_fulfillment",
    )
    release_date_from_lender = models.DateTimeField(null=True, blank=True)
    disburse_date_to_borrower = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        self.release_date_from_lender


class PaymentMethod(TimeBasedModel):
    pass
