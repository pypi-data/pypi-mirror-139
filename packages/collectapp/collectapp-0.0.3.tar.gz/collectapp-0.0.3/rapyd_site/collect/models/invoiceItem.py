from django.db import models
from .planCollect import Plan
from .invoice import Invoice


class InvoiceItem(models.Model):

    id = models.CharField(primary_key=True,
                          max_length=40,
                          verbose_name="ID_InvoiceItem")
    amount = models.FloatField()
    currency = models.CharField(max_length=40,
                                blank=True,
                                null=True,)
    date = models.IntegerField()
    description = models.CharField(max_length=200,
                                   blank=True,
                                   null=True,)
    discountable = models.BooleanField()
    metadata = models.JSONField(blank=True, null=True)
    period = models.JSONField()
    proration = models.BooleanField(blank=True, null=True)
    quantity = models.IntegerField()
    unit_amount = models.FloatField()
    subscription = models.CharField(max_length=40)
    customer = models.CharField(max_length=40)

    plan = models.ForeignKey(Plan,
                             blank=True,
                             null=True,
                             on_delete=models.CASCADE)
    invoice = models.ForeignKey(Invoice,
                                blank=True,
                                null=True,
                                on_delete=models.CASCADE)

    # plan = models.ForeignKey(Plan, on_delete=models.CASCADE)

    def __str__(self):
        return self.id
