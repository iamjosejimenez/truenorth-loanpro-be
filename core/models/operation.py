from django.db import models
from django.utils.translation import gettext_lazy as _

from .base import CustomAppManager, CustomBaseModel


class Operation(CustomBaseModel):
    """Operation object."""

    class OperationType(models.TextChoices):
        ADDITION = "ADDITION", _("Addition")
        SUBTRACTION = "SUBTRACTION", _("Subtraction")
        MULTIPLICATION = "MULTIPLICATION", _("Multiplication")
        DIVISION = "DIVISION", _("Division")
        SQUARE_ROOT = "SQUARE_ROOT", _("Square Root")
        RANDOM_STRING = "RANDOM_STRING", _("Random String")

    type = models.CharField(
        max_length=14,
        choices=OperationType.choices,
        unique=True,
    )
    cost = models.FloatField()

    objects = CustomAppManager()
