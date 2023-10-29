import auto_prefetch
from django.db import models
from django.utils import timezone

from kolopadi.utils.choices import SavingsFrequency, SavingsType
from kolopadi.utils.models import CategoryModel, NamedTimeBasedModel


class SavingsCategory(CategoryModel):
    class Meta(CategoryModel.Meta):
        verbose_name_plural = "Savings Categories"


class Savings(NamedTimeBasedModel):
    category = auto_prefetch.ForeignKey(
        SavingsCategory,
        on_delete=models.SET_NULL,
        null=True,
    )
    amount = models.PositiveIntegerField(default=0)
    target = models.PositiveIntegerField(default=0)
    frequency = models.CharField(max_length=50, choices=SavingsFrequency.choices)
    saving_type = models.CharField(max_length=50, choices=SavingsType.choices)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField()

    class Meta(auto_prefetch.Model.Meta):
        verbose_name_plural = "Savings"
