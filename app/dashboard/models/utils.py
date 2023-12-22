from django.db.models import Manager, QuerySet
from django.db import models


class AppQuerySet(QuerySet):
    def delete(self, hard=False):
        self.update(deleted=True)
        if hard:
            super().delete()


class AppManager(Manager):
    def get_queryset(self):
        return AppQuerySet(self.model, using=self._db) #.exclude(deleted=True)


class BaseModel(models.Model):
    class Meta:
        abstract = True
        # unique_together = ['id', 'deleted']

    id = models.AutoField(primary_key=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    def model_name(self):
        return self.__class__.__name__.lower()

    objects = AppManager()

    def delete(self, hard=False):
        self.deleted = True
        self.save()
        if hard:
            super().delete()
