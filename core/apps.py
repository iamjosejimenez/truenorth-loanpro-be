import logging

from django.apps import AppConfig
from django.conf import settings

logger = logging.getLogger(__name__)


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"

    def ready(self) -> None:
        logger.info("Loading default operations cost")
        Operation = self.models.get("operation")
        for operation_type in Operation.OperationType:
            logger.info("Loading %s cost", operation_type.value)
            operation_cost = getattr(settings, f"{operation_type}_COST", 1.00)

            Operation.objects.update_or_create(
                type=operation_type,
                defaults={"cost": operation_cost},
            )
            logger.info("Operation type %s loaded correctly", operation_type.value)

        return super().ready()
