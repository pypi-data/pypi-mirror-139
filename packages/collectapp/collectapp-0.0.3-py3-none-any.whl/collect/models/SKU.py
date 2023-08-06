from django.db import models
from .product import ProductCollect
# AGREGAR IMPORT FALTANTES


class SKU(models.Model):

    id = models.CharField(primary_key=True,
                          max_length=40,
                          verbose_name="ID_SKU")
    active = models.BooleanField(default=False)
    attributes = models.JSONField(blank=True, null=True)
    created_at = models.IntegerField(blank=True, null=True)
    currency = models.CharField(max_length=3)
    image = models.TextField(blank=True, null=True)
    inventory = models.JSONField()  # CHECK IT
    metadata = models.JSONField()  # JSON_OBJECT
    package_dimensions = models.JSONField()  # Other JSON_OBJECT
    price = models.FloatField()
    size = models.CharField(max_length=50, blank=True, null=True)
    updated_at = models.IntegerField(blank=True, null=True)

    product = models.ForeignKey(ProductCollect, on_delete=models.CASCADE)

    def __str__(self):
        return self.product
