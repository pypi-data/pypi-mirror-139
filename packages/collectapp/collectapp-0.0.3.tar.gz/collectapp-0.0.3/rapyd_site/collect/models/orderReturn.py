from django.db import models
from .SKU import SKU
from .order import Order
from .refund import Refund


class ReturnOrder(models.Model):

    id = models.CharField(primary_key=True,
                          max_length=40,
                          verbose_name="ID_ReturnOrder")
    amount = models.CharField(max_length=15)
    created = models.BigIntegerField()
    currency = models.CharField(max_length=3,
                                blank=True,
                                null=True)
    items = models.JSONField()

    order = models.ForeignKey(Order,
                              on_delete=models.CASCADE)
    refund = models.ForeignKey(Refund,
                               on_delete=models.CASCADE)
    # Todo

    def __str__(self):
        return self.DoesNotExist


class ReturnOrderItem(models.Model):

    type = models.CharField(max_length=10)
    amount = models.FloatField()
    currency = models.CharField(max_length=3)
    quantity = models.IntegerField()
    description = models.CharField(max_length=200)
    parent = models.ForeignKey(
        SKU,
        blank=True,
        null=True,
        on_delete=models.CASCADE)
    returnOrder = models.ForeignKey(
        ReturnOrder,
        on_delete=models.CASCADE)

    def __str__(self):
        return self.DoesNotExist
