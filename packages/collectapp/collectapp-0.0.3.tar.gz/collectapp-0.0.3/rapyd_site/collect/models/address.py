from django.db import models
from django_countries.fields import CountryField


class Address(models.Model):

    class Meta:
        verbose_name_plural = "addresses"

    id = models.CharField(primary_key=True,
                          max_length=50)
    canton = models.CharField(max_length=100,
                              null=True, blank=True)
    city = models.CharField(max_length=100,
                            null=True, blank=True)
    country = CountryField()
    created_at = models.IntegerField(null=True,
                                     blank=True)
    district = models.CharField(max_length=100,
                                null=True, blank=True)
    line_1 = models.CharField(max_length=255,
                              null=True, blank=True)
    line_2 = models.CharField(max_length=255,
                              null=True, blank=True)
    line_3 = models.CharField(max_length=255,
                              null=True, blank=True)
    metadata = models.JSONField(null=True, blank=True)
    name = models.CharField(max_length=100,
                            null=True, blank=True)
    phone_number = models.CharField(max_length=15,
                                    null=True, blank=True)
    state = models.CharField(max_length=100,
                             null=True, blank=True)
    updated_at = models.IntegerField(null=True,
                                     blank=True)
    zip = models.CharField(max_length=10,
                           null=True, blank=True)
