from django.db import models
from .suscriptionItem import SuscriptionItem


class UsageRecord(models.Model):

    id = models.CharField(primary_key=True,
                          max_length=40,
                          verbose_name="ID_Usage")
    action = models.CharField(max_length=10, blank=True, null=True)
    ending_before = models.IntegerField(blank=True, null=True)
    limit = models.IntegerField(default=10)
    quantity = models.IntegerField()  # relacionado con PLAN
    starting_after = models.IntegerField(blank=True, null=True)
    timestamp = models.IntegerField(blank=True, null=True)
    subscription_item = models.ForeignKey(
        SuscriptionItem,
        on_delete=models.CASCADE)

    def __str__(self):
        return self.DoesNotExist
