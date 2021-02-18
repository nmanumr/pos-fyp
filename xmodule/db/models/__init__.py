import inspect

from django.db.models import Model
from django.db.models.signals import class_prepared
from django.dispatch import receiver

from .fields import ChoiceEnum, ChoiceEnumField
from .soft_delete import SoftDeleteModel, SoftDeleteManager, SoftDeleteQuerySet
from .state_aware import StateAwareModel


@receiver(class_prepared)
def delete_default_permissions(sender, **kwargs):
    if not inspect.isclass(sender) or not issubclass(sender, Model):
        return

    sender._meta.default_permissions = ()
