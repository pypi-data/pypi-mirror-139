from django.db import models


class Escrow(models.Model):

    """El objeto Escrow representa los fondos retenidos en custodia
        para su liberación posterior. Se crea cuando se crea el pago.

        * El objecto Escrow contiene los siguientes campos:

            + id. "string": Id del depósito en garantía, una cadena
                    que comienza con "escrow".

            + amount. "number": Cantidad en custodia, en unidades definidas
                    por "currency". Decimal, incluido el número
                    correcto de lugares decimales para el exponente de
                    la moneda, tal como se define en la norma
                    ISO 2417:2015. Si la cantidad es un número entero,
                    use un número entero y no un decimal.

            + amount_on_hold. "number": Importe total de los fondos que se
                    mantienen actualmente en el depósito en garantía, en la
                    moneda definida en "currency_code".

            + created_at. "number": Hora de creación del depósito en garantia
                    en tiempo Unix. Solo respuesta.

            + escrow. "string": Id del depósito en garantía, una cadena
                    que comienza con "escrow".

            + escrow_release_days. "number": Indica el número de días después
                    de la creación del pago que los fondos se liberan del
                    depósito en garantía. Los fondos se liberan a las 5:00 p.m.
                    GMT del día indicado. Entero, rango: 1-90.

            + escrow_releases. "array": Matriz de objectos que describen
                    liberaciones individuales.
                    Consulte "Escrow Releases Object".

            + ewallets. "array": Matriz de objetos que definen la asignación
                    del lanzamiento a múltiples billeteras. Cada objeto
                    contiene los siguientes campos:

                        * ewallet. Id de la billetera, una cadena que comienza
                                con "ewallet".
                        * amount. La cantidad a liberar a esta billetera.
                                Relevante cuando "percentage" no está
                                establecido.

                        * percentage. El porcentaje de este depósito en
                                garantía para liberar a esta billetera.
                                Relevante cuando "amount" no está establecido.
                                En una liberación parcial posterior a la
                                primera, se refiere al porcentaje del monto
                                original del depósito en garantía.

                        Nota: Todas las billeteras en la matriz deben
                        especificarse por "amount" o "percentage" o ninguna.
                        Si no se fija ninunga, la liberación es proporcional
                        según el fraccionamiento definido en el pago.

            + last_payment_completion. "number": Hora de realización del
                    último pago o pago parcial en tiempo Unix.

            + payment. "string": Id del pago, una cadena que comienza con
                    "payment".

            + percentage. "number": El porcentaje que se paga a la billetera
                    del pago total. Decimal positivo, hasta 3 decimales.
                    Si la cantidad es un número entero, use un número entero y
                    no un decimal. Valor máximo: 100.

            + status. "string": Estado del depósito en garantía. Uno de los
                    siguientes:
                        * pending : se crearon el pago y el depósito en
                                garantía, pero el pago no se completó y
                                los fondos no están en el depósito en garantía.
                        * on_hold : el pago se completa y los fondos están en
                                depósito.
                        * canceled : el depósito en garantía está cancelado.
                        * released - Todos o parte de los fondos han sido
                                liberados a las carteras.

            + total_amount_released. "number": Cantidad total de fondos que se
                    liberaron en las billeteras en la moneda definida en
                    "currency_code".

            + updated_at. "number": Fecha y hora de la última actualización
                    del depósito en garantía en tiempo Unix.


    """

    id = models.CharField(primary_key=True, max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2,
                                 null=True, blank=True)
    amount_on_hold = models.DecimalField(max_digits=10, decimal_places=2,
                                         null=True, blank=True)
    created_at = models.BigIntegerField(null=True, blank=True)
    escrows = models.CharField(max_length=50, null=True, blank=True)
    escrow_release_days = models.IntegerField(null=True, blank=True)
    escrow_releases = models.TextField(null=True,
                                       blank=True)  # Array
    ewallets = models.TextField(null=True,
                                blank=True)  # Array
    last_payment_completion = models.BigIntegerField(null=True,
                                                     blank=True)
    payment = models.CharField(max_length=50,
                               null=True,
                               blank=True)  # id payment agregue "s"
    percentage = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=10, null=True, blank=True)
    total_amount_released = models.DecimalField(max_digits=10,
                                                decimal_places=2,
                                                null=True,
                                                blank=True)
    updated_at = models.BigIntegerField(null=True, blank=True)
