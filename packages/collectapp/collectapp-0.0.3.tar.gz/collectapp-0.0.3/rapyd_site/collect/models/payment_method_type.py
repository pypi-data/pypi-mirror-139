from django.db import models
from .address import Address


class PaymentMethodType(models.Model):

    id = models.CharField(primary_key=True,
                          max_length=50)
    amount_range_per_currency = models.JSONField(null=True,
                                                 blank=True)
    bin_details = models.JSONField(null=True, blank=True)
    category = models.CharField(max_length=100,
                                null=True, blank=True)
    country = models.CharField(max_length=100,
                               null=True, blank=True)
    currencies = models.JSONField(null=True, blank=True)
    customer = models.CharField(max_length=100,
                                null=True, blank=True)
    fields = models.JSONField(null=True, blank=True)
    fingerprint = models.CharField(max_length=100,
                                   null=True, blank=True)
    image = models.CharField(max_length=200,
                             null=True, blank=True)
    is_cancelable = models.BooleanField(default=True,
                                        null=True, blank=True)
    is_expirable = models.BooleanField(default=True,
                                       null=True, blank=True)
    is_online = models.BooleanField(default=True,
                                    null=True, blank=True)
    is_refundable = models.BooleanField(default=True,
                                        null=True, blank=True)
    is_tokenizable = models.BooleanField(default=True,
                                         null=True, blank=True)
    is_virtual = models.BooleanField(default=True,
                                     null=True, blank=True)
    last4 = models.CharField(max_length=100,
                             null=True, blank=True)
    maximun_expiration_seconds = models.IntegerField(null=True,
                                                     blank=True)
    minimun_expiration_seconds = models.IntegerField(null=True,
                                                     blank=True)
    multiple_overage_allowed = models.BooleanField(default=True,
                                                   null=True,
                                                   blank=True)
    name = models.CharField(max_length=100,
                            null=True, blank=True)
    payment_flow_type = models.CharField(max_length=100,
                                         null=True,
                                         blank=True)
    payment_method_options = models.JSONField(null=True,
                                              blank=True)
    payment_options = models.JSONField(null=True, blank=True)
    status = models.IntegerField(null=True, blank=True)
    supported_digital_wallet_providers = models.JSONField(null=True,
                                                          blank=True)
    type = models.CharField(max_length=100, null=True, blank=True)
    virtual_payment_method_type = models.CharField(max_length=100,
                                                   null=True,
                                                   blank=True)

    address = models.ForeignKey(Address, on_delete=models.CASCADE)
