from django.db import models
from .customer import Customer
from .suscriptionCollect import SuscriptionCollect


class Invoice(models.Model):

    id = models.CharField(primary_key=True,
                          max_length=40,
                          verbose_name="ID_Invoice")
    attempt_count = models.IntegerField(blank=True, null=True)
    attempted = models.BooleanField(default="pay_automatically")
    billing = models.CharField(max_length=40)
    billing_reason = models.CharField(max_length=40, blank=True, null=True)
    created_at = models.BigIntegerField(blank=True, null=True)
    currency = models.CharField(blank=True, null=True, max_length=3)
    days_until_due = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    discount = models.TextField(blank=True, null=True)
    due_date = models.IntegerField(blank=True, null=True)
    lines = models.TextField(blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)
    next_payment_attempt = models.BigIntegerField(blank=True, null=True)
    number = models.CharField(
        max_length=40)  # PREFIX REFERED FROM CUSTOMER
    payment = models.JSONField(blank=True, null=True)
    payment_fields = models.JSONField(blank=True, null=True)
    payment_method = models.CharField(max_length=40,
                                      blank=True,
                                      null=True)
    payout = models.CharField(max_length=40,
                              blank=True,
                              null=True)
    payout_fields = models.JSONField(max_length=40,
                                     blank=True,
                                     null=True)
    period_end = models.CharField(
        max_length=40,
        blank=True,
        null=True)  # in unix field
    period_start = models.CharField(max_length=40, blank=True, null=True)
    statement_descriptor = models.CharField(max_length=100,
                                            blank=True,
                                            null=True)
    status = models.CharField(max_length=12,
                              blank=True,
                              null=True)
    subtotal = models.IntegerField()
    tax = models.FloatField()
    tax_percent = models.FloatField(blank=True, null=True)
    total = models.FloatField()
    type = models.CharField(max_length=10)

    subscription = models.ForeignKey(
        SuscriptionCollect,
        blank=True,
        null=True,
        on_delete=models.CASCADE)
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE)

    def __str__(self):
        return self.DoesNotExist
