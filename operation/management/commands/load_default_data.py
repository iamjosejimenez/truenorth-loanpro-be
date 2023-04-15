import logging

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from core.models import Operation

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = (
        "Loads default operations, taking its cost from external envitoment variables"
    )

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        logger.info("Loading default operations cost")
        for operation_type in Operation.OperationType:
            logger.info("Loading %s cost", operation_type.value)
            operation_cost = getattr(settings, f"{operation_type}_COST", 1.00)

            Operation.objects.update_or_create(
                type=operation_type,
                defaults={"cost": operation_cost},
            )
            logger.info("Operation type %s loaded correctly", operation_type.value)
