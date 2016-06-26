from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

# Create your models here.

class PartnerManager(models.Manager):
    def create_partner(self, name, consent, b):
        p = self.create(
            name=name, reg_date=timezone.now(), brief=b, consent=consent
            )
        return p

class Partner(models.Model):
    name = models.CharField(max_length=200)
    reg_date = models.DateTimeField('date registered')
    brief = models.IntegerField(default=-1)
    consent = models.BooleanField(default=False)

    objects = PartnerManager()

    def __str__(self):
        return self.name
