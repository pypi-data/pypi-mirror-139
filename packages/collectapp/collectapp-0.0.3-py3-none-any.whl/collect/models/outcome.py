from django.db import models


class Outcome(models.Model):

    network_status = models.CharField(max_length=30,
                                      blank=True,
                                      null=True)
    risk_level = models.CharField(max_length=20,
                                  blank=True,
                                  null=True)
    seller_message = models.CharField(max_length=50,
                                      blank=True,
                                      null=True)
    type = models.CharField(max_length=30,
                            blank=True,
                            null=True)
    reason = models.CharField(max_length=50,
                              blank=True,
                              null=True)
