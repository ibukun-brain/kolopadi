import uuid

import auto_prefetch
from django.contrib.auth import get_user_model
from django.db import models
from django.forms import ValidationError

from kolopadi.utils.choices import (
    TransactionType,
    TransferStatus,
    VTPassTransactionStatus,
)
from kolopadi.utils.models import NamedTimeBasedModel, TimeBasedModel

User = get_user_model()


class Bank(NamedTimeBasedModel):
    bank_code = models.CharField(max_length=10)

    class Meta(auto_prefetch.Model.Meta):
        ordering = ["name"]
        indexes = [models.Index(fields=["name"])]

    def __str__(self):
        return self.name


class Wallet(TimeBasedModel):
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    user = auto_prefetch.OneToOneField("home.CustomUser", on_delete=models.CASCADE)
    account_name = models.CharField(max_length=250, blank=True)
    account_number = models.CharField(max_length=10, blank=True)
    account_reference = models.CharField(max_length=50)
    barter_id = models.CharField(max_length=20)
    balance = models.DecimalField(
        decimal_places=2,
        max_digits=11,
        default=0.00,
    )
    bank = models.CharField(max_length=20, blank=True)
    is_hidden = models.BooleanField(default=False)
    pin = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.account_name}"


class Transaction(TimeBasedModel):
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    wallet = auto_prefetch.ForeignKey(
        Wallet, on_delete=models.CASCADE, related_name="transaction"
    )
    type = models.CharField(max_length=50, choices=TransactionType.choices)
    balance_before = models.DecimalField(
        decimal_places=2, max_digits=11, blank=True, null=True
    )
    balance_after = models.DecimalField(
        decimal_places=2, max_digits=11, blank=True, null=True
    )
    amount = models.CharField(max_length=50, blank=True)
    remarks = models.TextField(blank=True)
    reference = models.CharField(max_length=50, blank=True)
    date = models.DateField(
        blank=True,
        null=True,
        help_text="The transaction date from flutterwave or vtpass",
    )
    vt_pass_request_id = models.CharField(
        max_length=50, blank=True, help_text="For querying transaction status on vtpass"
    )
    vtpass_transaction_id = models.CharField(
        max_length=50,
        blank=True,
    )
    transfer_status = models.CharField(
        max_length=50, blank=True, choices=TransferStatus.choices
    )
    vtpass_status = models.CharField(
        max_length=50, choices=VTPassTransactionStatus.choices, blank=True
    )
    phone_number = models.CharField(max_length=15, blank=True)
    # bill_service = auto_prefetch.ForeignKey(
    #     "bill.BillService",
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     blank=True,
    #     help_text="Bill service that was paid for",
    # )
    external_recipient = models.CharField(max_length=100, blank=True)
    external_recipient_account_no = models.CharField(max_length=10, blank=True)
    external_recipient_bank = models.CharField(max_length=100, blank=True)
    recipient_wallet = auto_prefetch.ForeignKey(
        "wallets.Wallet",
        on_delete=models.SET_NULL,
        related_name="transaction_recipient",
        null=True,
        blank=True,
        help_text="Store recipient wallet if the sender is a member",
    )

    class Meta(auto_prefetch.Model.Meta):
        ordering = ("-date", "-created_at")
        indexes = [
            models.Index(fields=["-date", "-created_at"]),
        ]

    def __str__(self):
        return f"{self.wallet} transactions"

    @property
    def edit_remark(self):
        remarks = self.remarks
        text = remarks.split("|")[0].title()
        text = text.replace("Received Money", " Transfer ")
        return text

    @property
    def format_amount(self):
        amount = float(self.amount)
        return "{0:.2f}".format(amount)

    @property
    def sender_details(self):
        bank = None
        sender = None
        if self.type == "C":
            try:
                bank, sender = (
                    self.remarks.split("|")[0].split(" from ")[1],
                    self.remarks.split("|")[1],
                )
            except IndexError:
                pass
        return (bank, sender)


class SecurityQuestion(TimeBasedModel):
    question = models.CharField(max_length=100)
    uid = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        if self.question == "other":
            return self.custom_question
        return self.question


class WalletSecurity(TimeBasedModel):
    wallet = auto_prefetch.OneToOneField(
        Wallet, on_delete=models.SET_NULL, null=True, related_name="wallet_security"
    )
    security_question = auto_prefetch.ForeignKey(
        SecurityQuestion, on_delete=models.SET_NULL, null=True
    )
    custom_security_question = models.CharField(max_length=100, blank=True)
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    answer = models.CharField(max_length=50)

    class Meta(auto_prefetch.Model.Meta):
        verbose_name_plural = "Wallet Security"

    def clean(self):
        if (
            self.security_question.question == "Other"
            and self.custom_security_question == ""
        ):
            raise ValidationError("Custom question cannot be blank!")

    def __str__(self):
        return f"{self.wallet} security question"
