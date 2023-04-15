from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from .base import CustomAppManager, CustomBaseModel


class Record(CustomBaseModel):
    """Record object."""

    operation_id = models.ForeignKey(
        "core.operation",
        on_delete=models.CASCADE,
    )
    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    amount = models.FloatField()
    user_balance = models.FloatField()
    operation_response = models.CharField(max_length=32)
    data = models.DateTimeField(auto_now_add=True)
    objects = CustomAppManager()
