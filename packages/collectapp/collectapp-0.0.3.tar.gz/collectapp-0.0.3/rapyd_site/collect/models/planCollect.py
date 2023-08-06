from django.db import models
from .product import ProductCollect  # noqa


class Plan(models.Model):

    id = models.CharField(primary_key=True,
                          max_length=41,
                          verbose_name="ID_Plan")  # Relative key
    aggregate_usage = models.CharField(max_length=40, blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    billing_scheme = models.CharField(max_length=40, default='per_unit')
    created_at = models.IntegerField()  # duda referente [Response Only]
    currency = models.CharField(max_length=3)
    interval = models.CharField(max_length=40)  # duda referente
    interval_count = models.IntegerField()
    metadata = models.JSONField(blank=True, null=True)
    nickname = models.CharField(max_length=40)
    tiers = models.TextField(max_length=40, blank=True, null=True)
    tiers_mode = models.CharField(max_length=50)
    transform_usage = models.JSONField()  # DUDA OBJECT
    trial_period_days = models.PositiveIntegerField()
    usage_type = models.CharField(max_length=40, default='licensed')
    product = models.ForeignKey(
        ProductCollect,
        on_delete=models.CASCADE)

    def __str__(self):
        return self.idPlan
