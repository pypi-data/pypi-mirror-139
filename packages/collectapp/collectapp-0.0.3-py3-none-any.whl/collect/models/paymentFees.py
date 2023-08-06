from django.db import models


class TransactionFee(models.Model):

    calc_type = models.CharField(max_length=10,
                                 null=True,
                                 blank=True)
    fee_type = models.CharField(max_length=15,
                                null=True,
                                blank=True)
    value = models.DecimalField(max_digits=10,
                                decimal_places=2,
                                null=True,
                                blank=True)


class FxFee(models.Model):

    calc_type = models.CharField(max_length=10,
                                 null=True,
                                 blank=True)
    value = models.IntegerField(null=True,
                                blank=True)


class PaymentFee(models.Model):

    gross_fees = models.IntegerField(null=True,
                                     blank=True)
    net_fess = models.IntegerField(null=True,
                                   blank=True)
    fx_fee = models.ForeignKey(FxFee,
                               on_delete=models.CASCADE,
                               blank=True,
                               null=True)
    transaction_fee = models.ForeignKey(
        TransactionFee,
        on_delete=models.CASCADE,
        blank=True,
        null=True)
