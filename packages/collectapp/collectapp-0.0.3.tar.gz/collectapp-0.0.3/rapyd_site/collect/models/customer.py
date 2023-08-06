from django.db import models
from .address import Address
from .coupon import Coupon
# from collect.models.customer_payment_method import Customer_payment_method


class Customer(models.Model):

    id = models.CharField(primary_key=True,
                          max_length=50)
    addresses = models.JSONField(null=True, blank=True)
    business_vat_id = models.CharField(max_length=50,
                                       null=True, blank=True)
    category = models.CharField(max_length=50,
                                null=True, blank=True)
    coupon = models.CharField(max_length=50,
                              null=True, blank=True)
    created_at = models.IntegerField(null=True, blank=True)
    customer = models.CharField(max_length=100,
                                null=True, blank=True)
    default_payments_method = models.JSONField(null=True,
                                               blank=True)
    delinquent = models.BooleanField(default=True,
                                     null=True, blank=True)
    description = models.CharField(max_length=200,
                                   null=True, blank=True)
    email = models.CharField(max_length=512,
                             null=True, blank=True)
    ewallet = models.CharField(max_length=100,
                               null=True, blank=True)
    fields = models.JSONField(null=True, blank=True)
    invoice_prefix = models.CharField(max_length=50,
                                      null=True, blank=True)
    metadata = models.JSONField(null=True, blank=True)
    name = models.CharField(max_length=100,
                            null=True, blank=True)
    next_action = models.CharField(max_length=100,
                                   null=True, blank=True)
    payment_methods = models.JSONField(null=True, blank=True)
    phone_number = models.CharField(max_length=15,
                                    null=True, blank=True)
    redirect_url = models.CharField(max_length=200,
                                    null=True, blank=True)
    subscriptions = models.JSONField(null=True, blank=True)
    token = models.CharField(max_length=100,
                             null=True, blank=True)
    type = models.CharField(max_length=100,
                            null=True, blank=True)

    address = models.ForeignKey(Address,
                                on_delete=models.CASCADE,
                                null=True, blank=True)
    discount = models.ForeignKey(Coupon,
                                 on_delete=models.CASCADE,
                                 null=True, blank=True)
