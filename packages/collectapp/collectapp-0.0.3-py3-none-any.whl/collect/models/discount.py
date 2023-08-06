from django.db import models
from collect.models.coupon import Coupon


class Discount(models.Model):

    id = models.CharField(primary_key=True,
                          max_length=50,)

    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
