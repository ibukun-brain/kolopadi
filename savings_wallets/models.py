import uuid
from decimal import Decimal

import auto_prefetch
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone

from kolopadi.utils.choices import SavingsFrequency, SavingsStatus, SavingsType
from kolopadi.utils.models import CategoryModel, NamedTimeBasedModel


class SavingsCategory(CategoryModel):
    class Meta(CategoryModel.Meta):
        verbose_name_plural = "Savings Categories"


class Savings(NamedTimeBasedModel):
    uid = models.UUIDField(default=uuid.uuid4)
    user = auto_prefetch.ForeignKey("home.CustomUser", on_delete=models.CASCADE)
    category = auto_prefetch.ForeignKey(
        SavingsCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    frequency_amount = models.DecimalField(
        decimal_places=2,
        max_digits=11,
        default=0.00,
        validators=[MinValueValidator(Decimal("100.00"))],
    )
    amount_saved = models.DecimalField(decimal_places=2, max_digits=11, default=0.00)
    amount_to_save = models.DecimalField(decimal_places=2, max_digits=11, default=0.00)
    type_of_savings = models.CharField(max_length=50)
    frequency = models.CharField(max_length=50, choices=SavingsFrequency.choices)
    type_of_savings = models.CharField(max_length=50, choices=SavingsType.choices)
    start_date = models.DateField(default=timezone.now)
    status = models.CharField(
        max_length=50, choices=SavingsStatus.choices, default=SavingsStatus.Started
    )
    end_date = models.DateField()
    is_liquidated = models.BooleanField(default=False)

    class Meta(auto_prefetch.Model.Meta):
        verbose_name_plural = "Savings"
        ordering = ["created_at", "start_date"]
        indexes = [
            models.Index(
                fields=["created_at", "start_date"],
            )
        ]

    @property
    def next_savings_date(self):
        if self.start_date:
            if self.frequency == "daily":
                next_date = timezone.now().date() + timezone.timedelta(days=1)
            elif self.frequency == "weekly":
                next_date = self.start_date + timezone.timedelta(days=7)
            elif self.frequency == "monthly":
                next_date = self.start_date + timezone.timedelta(days=1)
        return next_date
