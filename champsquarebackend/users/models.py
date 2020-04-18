from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
# Create your models here.

class User(AbstractUser):
    name = models.CharField(_("Name of the user"), blank=True, max_length=100)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})
    
