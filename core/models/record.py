from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from .base import CustomAppManager, CustomBaseModel


class Record(CustomBaseModel):
    """Record object."""

    operation = models.ForeignKey(
        "core.Operation",
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    amount = models.FloatField()
    user_balance = models.FloatField()
    operation_response = models.CharField(max_length=32)
    date = models.DateTimeField(auto_now_add=True)

    objects = CustomAppManager()
