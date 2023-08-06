from django.db import models


class PaymentMethodData(models.Model):

    id = models.CharField(
        primary_key=True,
        max_length=40)
    acs_check = models.CharField(max_length=15,
                                 null=True, blank=True)
    avs_check = models.CharField(max_length=15, null=True, blank=True)
    authentication_url = models.CharField(max_length=80,
                                          null=True, blank=True)
    bit_details = models.JSONField(null=True, blank=True)
    category = models.CharField(max_length=20, null=True, blank=True)
    expiration_month = models.CharField(max_length=2,
                                        null=True, blank=True)
    expiration_year = models.CharField(max_length=2,
                                       null=True, blank=True)
    fingerprint_token = models.CharField(max_length=40,
                                         null=True, blank=True)
    image = models.CharField(max_length=80, null=True, blank=True)
    last4 = models.CharField(max_length=4, null=True, blank=True)
    metadata = models.JSONField(null=True, blank=True)
    network_reference_id = models.CharField(max_length=20,
                                            null=True, blank=True)
    next_action = models.CharField(max_length=25, null=True, blank=True)
    type = models.CharField(max_length=40, null=True, blank=True)
    supporting_documentation = models.CharField(max_length=20,
                                                null=True, blank=True)
    webhook_url = models.CharField(max_length=80, null=True, blank=True)
