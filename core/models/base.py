from django.db import models


class CustomAppQuerySet(models.QuerySet):
    """Custom App Query Set adapted to application needs"""

    def delete(self):
        self.update(is_deleted=True)


class CustomAppManager(models.Manager):
    """Custom App Manager adapted to application needs"""

    def get_queryset(self):
        return CustomAppQuerySet(self.model, using=self._db).exclude(is_deleted=True)


class CustomBaseModel(models.Model):
    """Custom Base Model adapted to application needs"""

    class Meta:
        abstract = True

    is_deleted = models.BooleanField(default=False)

    objects = CustomAppManager()

    def delete(self):
        """Mark the record as deleted instead of actually deleting it"""

        self.is_deleted = True
        self.save()
