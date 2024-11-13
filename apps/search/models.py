from django.db import models

# Create your models here.

from django.db import models


class Search(models.Model):
    name = models.CharField(max_length=255)