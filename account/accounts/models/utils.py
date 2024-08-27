from django.db import models

from datetime import datetime
from django.utils.translation import gettext_lazy as _

import uuid

class TimeStamp(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    flag = models.IntegerField(_("is_active"), default=1, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# World
class TimeZone(TimeStamp):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        db_table = 'time_zone'

class countries(TimeStamp):
    name = models.CharField(max_length=50)
    shortname = models.CharField(max_length=10)
    phonecode = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        db_table = 'countries'

class states(TimeStamp):
    country_id = models.ForeignKey(countries, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        db_table = 'states'

class cities(TimeStamp):
    state_id = models.ForeignKey(states, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        db_table = 'cities'