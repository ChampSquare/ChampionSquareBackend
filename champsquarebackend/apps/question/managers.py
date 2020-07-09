from django.db import models
from django.db.models import Count

class BrowsableQuestionManager(models.Manager):
    """ Returns questions which are active """
    active_filter = True

    def get_queryset(self):
        return super().get_queryset().filter(
            active=self.active_filter)
