from django.db import models
from .SKU import SKU
from .coupon import Coupon
from .customer import Customer
from .payment import Payment


class Order(models.Model):

    id = models.CharField(primary_key=True,
                          max_length=40,
                          verbose_name="ID_ItemOrder")
    amount = models.FloatField()  # dual mode operation
    amount_returned = models.FloatField()
    created = models.BigIntegerField()
    currency = models.CharField(max_length=3)
    discount = models.CharField(
        max_length=40,
        blank=True,
        null=True,)
    email = models.CharField(max_length=50)
    external_coupon_code = models.CharField(
        blank=True,
        null=True,
        max_length=40)  # id coupon, defined by merchant
    metadata = models.JSONField(blank=True, null=True)  # metadata
    returns = models.TextField(blank=True, null=True)
    shipping_address = models.JSONField(blank=True, null=True)  # cambien json
    status = models.CharField(max_length=12)
    status_transitions = models.JSONField(
        blank=True, null=True)  # UNIX TIME
    tax_percent = models.FloatField()
    updated = models.BigIntegerField(blank=True, null=True)
    upstream_id = models.CharField(max_length=100)
    payment_method = models.CharField(
        blank=True,
        null=True,
        max_length=50)

    coupon = models.ForeignKey(
        Coupon,
        blank=True,
        null=True,
        on_delete=models.CASCADE)
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE)
    payments = models.ForeignKey(
        Payment,
        blank=True,
        null=True,
        on_delete=models.CASCADE)

    def __str__(self):
        return self.id


class ItemOrder(models.Model):

    type = models.CharField(max_length=10)
    amount = models.FloatField()  # defined as SKU UNIT PRICE
    currency = models.CharField(max_length=3)  # ISO 4217 CODE CURRENCY
    quantity = models.IntegerField()  # requested if is SKU product
    description = models.CharField(max_length=200)

    parent = models.ForeignKey(
        SKU,
        blank=True,
        null=True,
        on_delete=models.CASCADE)
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE)

    def __str__(self):
        return self.DoesNotExist
