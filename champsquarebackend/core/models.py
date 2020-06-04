from typing import Any

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import JSONField

class ModelWithMetadata(models.Model):
    """
    An abstract class to be extended to add metadata to models
    """
    metadata = JSONField(_("used to store metadata"), blank=True, null=True, default=dict)
    
    class Meta:
        abstract = True

    def get_value_from_metadata(self, key: str, default: Any = None) -> Any:
        return self.metadata.get(key, default)

    def store_value_in_metadata(self, items: dict):
        if not self.metadata:
            self.metadata = {}
        self.metadata.update(items)

    def clear_metadata(self):
        self.metadata = {}

    def delete_value_from_metadata(self, key: str):
        if key in self.metadata:
            del self.metadata[key]



class TimestampedModel(models.Model):
    """
    An abstract class to be extended to add timestamp to models
    """
    # auto_now_add will set the timezone.now() only when the instance is created
    created_at = models.DateTimeField(_("datetime when model is created"), 
                                        auto_now_add=True)
    # auto_now will update the field everytime the save method is called.
    update_at = models.DateTimeField(_("datetime when model is updated last time"), 
                                        auto_now=True)

    class Meta:
        abstract = True
