from django.db import models
from .customer import Customer


class HostedPageCardToken(models.Model):

    id = models.CharField(primary_key=True,
                          max_length=50)
    billing_address_collect = models.BooleanField(default=True,
                                                  null=True, blank=True)
    cancel_url = models.CharField(max_length=100,
                                  null=True, blank=True)
    category = models.CharField(max_length=100,
                                null=True, blank=True)
    complete_url = models.CharField(max_length=100,
                                    null=True, blank=True)
    country = models.CharField(max_length=100,
                               null=True, blank=True)
    currency = models.CharField(max_length=100,
                                null=True, blank=True)
    error_code = models.CharField(max_length=100,
                                  null=True, blank=True)
    language = models.CharField(max_length=100,
                                null=True, blank=True)
    merchant_alias = models.CharField(max_length=100,
                                      null=True, blank=True)
    merchant_color = models.CharField(max_length=100,
                                      null=True, blank=True)
    merchant_customer_support = models.JSONField(null=True,
                                                 blank=True)
    merchant_logo = models.CharField(max_length=100, null=True,
                                     blank=True)
    merchant_website = models.CharField(max_length=100,
                                        null=True, blank=True)
    page_expiration = models.IntegerField(null=True, blank=True)
    payment_method_type = models.CharField(max_length=100,
                                           null=True, blank=True)
    payment_params = models.JSONField(null=True, blank=True)
    redirect_url = models.CharField(max_length=100,
                                    null=True, blank=True)
    status = models.CharField(max_length=100,
                              null=True, blank=True)

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
