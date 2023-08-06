from django.db import models


class GroupPayment(models.Model):

    """El objeto Pago grupal describe un pago en el que los fondos
        se cobran de dos a diez métodos de pago.

        * El objeto pago de grupo contiene los siguientes campos:

            + id. "string": Id del objeto pago de grupo. Cadena
                    que comienza con "gp".

            + amount: Monto del pago, en unidades definidas
                    por "currency". Decimal, incluido el número
                    correcto de lugares decimales para el exponente de
                    la moneda, tal como se define en la norma
                    ISO 2417:2015. Si la cantidad es un número entero,
                    use un número entero y no un decimal.

            + amount_to_replace. "string": Indica la cantidad de pagos
                    fallidos que no han sido reemplazados.Solo
                    respuesta.

            + cancel_reason. "string": Motivo de la cancelación del pago.
                    Solo respuesta.

            + country. "string": País de los metodo de pago. Código ISO
                    3166-1 ALPHA-2 de dos letras. Solo respuesta.

            + country_code. "string": País de los metodo de pago. Código ISO
                    3166-1 ALPHA-2 de dos letras. Solo respuest.

            + currency. "string": Moneda de los pagos. Codigo ISO 4217 de
                    tres letras.

            + currency_code."string". Moneda de los pagos. Codigo ISO 4217 de
                    tres letras.

            + description. "string": Descripción del pago de grupo.

            + expiration. "number": Fin del tiempo permitido para que los
                    clientes realicen el pago en tiempo Unix. Solo respuesta.

            + merchant_reference_id. "string": Identificación definida por
                    el comerciante. Limitado a 255 caracteres.

            + metadata. "object": Un objeto JSON definido por el cliente.

            + payments: "array of objects": Matriz de objetos de pago. Todos
                    los pagos deben tener la misma moneda y deben admitirse
                    en el mismo país.

                    Para obtener más información, consulte "Payment Object".

            + reason. "string": Motivo de la cancelación del pago de grupo.

            + status. "string": Indica el estado de la operación de pago del
                    grupo. Uno de los siguientes valores:
                        * active : el pago grupal se creó y uno o más pagos
                                aún están abiertos.
                        * canceled - El pago del grupo fue cancelado.
                        * closed : todos los pagos en el pago grupal están
                                completos.

    """
    id = models.CharField(primary_key=True,
                          max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2,
                                 null=True, blank=True)
    amount_to_replace = models.CharField(max_length=5,
                                         null=True,
                                         blank=True)
    cancel_reason = models.CharField(max_length=20,
                                     null=True,
                                     blank=True)
    country = models.CharField(max_length=2,
                               null=True,
                               blank=True)
    country_code = models.CharField(max_length=2,
                                    null=True,
                                    blank=True)
    currency = models.CharField(max_length=3,
                                null=True, blank=True)
    currency_code = models.CharField(max_length=3,
                                     null=True, blank=True)
    description = models.CharField(max_length=20,
                                   null=True, blank=True)
    expiration = models.BigIntegerField(null=True, blank=True)
    merchant_reference_id = models.CharField(max_length=255,
                                             null=True,
                                             blank=True)
    metadata = models.JSONField(null=True, blank=True)  # Json Object
    payments = models.TextField(null=True, blank=True)  # Array of objects
    reason = models.CharField(max_length=20, null=True, blank=True)
    status = models.CharField(max_length=10, null=True, blank=True)
