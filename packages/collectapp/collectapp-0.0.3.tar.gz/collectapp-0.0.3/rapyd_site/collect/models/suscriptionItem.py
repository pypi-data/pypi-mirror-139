from django.db import models
from .planCollect import Plan
from .suscriptionCollect import SuscriptionCollect


class SuscriptionItem(models.Model):

    id = models.CharField(primary_key=True,
                          max_length=40,
                          verbose_name="ID_SubscriptionItem")
    created = models.IntegerField(blank=True, null=True)  # UNIX TIME
    metadata = models.JSONField(blank=True, null=True)  # JSON OBJECT
    prorate = models.BooleanField(blank=True, null=True)
    proration_date = models.IntegerField(blank=True, null=True)  # UNIX TIME
    quantity = models.IntegerField(blank=True, null=True)

    plan = models.ForeignKey(Plan,
                             on_delete=models.CASCADE)
    subscription = models.ForeignKey(
        SuscriptionCollect,
        on_delete=models.CASCADE)

    # Todo
    def __str__(self):
        return self.id
