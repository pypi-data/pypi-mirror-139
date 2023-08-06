from django.db import models


class Coupon(models.Model):

    id = models.CharField(primary_key=True,
                          max_length=50)
    amount_off = models.IntegerField(null=True,
                                     blank=True)
    created = models.IntegerField(null=True,
                                  blank=True)
    currency = models.CharField(max_length=100,
                                null=True, blank=True)
    deleted = models.BooleanField(default=True,
                                  null=True, blank=True)
    duration = models.CharField(max_length=100,
                                null=True, blank=True)
    duration_in_months = models.IntegerField(null=True,
                                             blank=True)
    max_redemptions = models.IntegerField(null=True,
                                          blank=True)
    metadata = metadata = models.JSONField(null=True,
                                           blank=True)
    percent_off = models.IntegerField(null=True,
                                      blank=True)
    redeem_by = models.IntegerField(null=True,
                                    blank=True)
    times_redeemed = models.IntegerField(null=True,
                                         blank=True)
    valid = models.BooleanField(default=True, null=True,
                                blank=True)
