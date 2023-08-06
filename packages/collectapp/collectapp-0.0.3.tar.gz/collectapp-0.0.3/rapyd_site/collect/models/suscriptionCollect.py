# from http.client import PAYMENT_REQUIRED
from django.db import models
from .customer import Customer
from .coupon import Coupon


class SuscriptionCollect(models.Model):

    id = models.CharField(primary_key=True,
                          max_length=40,
                          verbose_name="ID_Suscription")
    billing = models.CharField(max_length=40)
    billing_cycle_anchor = models.CharField(
        max_length=40)
    cancel_at_period_end = models.BooleanField(
        default=False)
    canceled_at = models.IntegerField(
        blank=True,
        null=True)  # unix time or number in unix time
    created_at = models.IntegerField(
        blank=True,
        null=True)  # UNIX TIME
    current_period_end = models.IntegerField(
        blank=True,
        null=True)  # UNIX TIME
    current_period_start = models.IntegerField(
        blank=True,
        null=True)  # UNIX TIME
    customer_token = models.CharField(
        max_length=40,
        blank=True,
        null=True)  # TRAER DE CUSTOMER TOKEN
    days_until_due = models.IntegerField(
        blank=True,
        null=True)
    discount = models.CharField(max_length=40)
    ended_at = models.IntegerField(
        blank=True,
        null=True)  # unix time
    metadata = models.JSONField(
        blank=True,
        null=True)  # JSON OBJECT
    # RESERVADO EN DOC.
    payout_fields = models.JSONField(blank=True, null=True)
    payment_fields = models.JSONField(blank=True, null=True)
    payment_method = models.CharField(max_length=40, blank=True, null=True)
    start = models.IntegerField(
        blank=True,
        null=True)  # UNIX TIME
    status = models.CharField(max_length=10)
    subscription_items = models.JSONField()  # ARRAY OF OBJECTS CHECK
    tax_percent = models.FloatField()  # definir en porcentaje
    total_count = models.IntegerField(editable=False)
    trial_end = models.IntegerField(blank=True,
                                    null=True)
    trial_from_plan = models.BooleanField(default=False)
    trial_period_days = models.IntegerField(blank=True,
                                            null=True)  # max 773
    trial_start = models.IntegerField(blank=True,
                                      null=True)
    type = models.CharField(max_length=10,
                            blank=True, null=True)

    coupon = models.ForeignKey(Coupon,
                               blank=True,
                               null=True,
                               on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,
                                 on_delete=models.CASCADE)

    def __str__(self):
        return self.DoesNotExist  # aun no definido
