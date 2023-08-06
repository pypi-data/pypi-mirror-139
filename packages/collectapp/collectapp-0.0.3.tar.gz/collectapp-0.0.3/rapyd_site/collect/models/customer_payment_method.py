from django.db import models
from .address import Address


class CustomerPaymentMethod(models.Model):

    id = models.CharField(primary_key=True,
                          max_length=50)
    category = models.CharField(max_length=100,
                                null=True, blank=True)
    customer = models.CharField(max_length=200,
                                null=True, blank=True)
    deleted = models.BooleanField(default=True,
                                  null=True, blank=True)
    ending_before = models.CharField(max_length=100,
                                     null=True, blank=True)
    error_code = models.CharField(max_length=100,
                                  null=True, blank=True)
    fields = models.JSONField(null=True, blank=True)
    image = models.CharField(max_length=100,
                             null=True, blank=True)
    limit = models.CharField(max_length=100,
                             null=True, blank=True)
    metadata = models.JSONField(null=True, blank=True)
    network_referenci_id = models.CharField(max_length=100,
                                            null=True, blank=True)
    next_action = models.CharField(max_length=100,
                                   null=True, blank=True)
    payment_methods = models.CharField(max_length=100,
                                       null=True, blank=True)
    redirect_url = models.CharField(max_length=100,
                                    null=True, blank=True)
    starting_after = models.CharField(max_length=100,
                                      null=True, blank=True)

    supporting_documentation = models.CharField(max_length=100,
                                                null=True,
                                                blank=True)
    token = models.CharField(max_length=100,
                             null=True, blank=True)
    types = models.CharField(max_length=100,
                             null=True, blank=True)
    webhook_url = models.CharField(max_length=100,
                                   null=True, blank=True)

    address = models.ForeignKey(Address, on_delete=models.CASCADE)
