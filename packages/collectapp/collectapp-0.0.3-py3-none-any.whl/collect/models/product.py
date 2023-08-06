from django.db import models


class ProductCollect(models.Model):

    id = models.CharField(primary_key=True,
                          max_length=40,
                          verbose_name="ID_Product")
    active = models.BooleanField(blank=True,
                                 null=True)
    attributes = models.TextField(blank=True,
                                  null=True)  # ARRAY OF STRING
    created_at = models.IntegerField(
        blank=True,
        null=True)  # unix time
    description = models.CharField(blank=True,
                                   null=True,
                                   max_length=200)
    images = models.TextField(blank=True,
                              null=True)  # ARRAY OF OBJECTS
    metadata = models.JSONField(blank=True,
                                null=True)
    name = models.CharField(blank=True,
                            null=True,
                            max_length=100)
    package_dimensions = models.JSONField(
        blank=True,
        null=True)
    shippable = models.BooleanField(blank=True,
                                    null=True)
    skus = models.TextField(
        blank=True,
        null=True)  # ARREGLO DE SKUS
    statement_descriptor = models.CharField(
        max_length=40,
        blank=True,
        null=True)
    type = models.CharField(max_length=10, blank=True,
                            null=True)
    unit_label = models.CharField(max_length=40,
                                  blank=True,
                                  null=True)
    updated_at = models.IntegerField(
        blank=True,
        null=True)
