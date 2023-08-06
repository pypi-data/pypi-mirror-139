from django.db import models


class Dispute(models.Model):

    """El objeto Disputa describe una única disputa que se realiza
        contra un pago con tarjeta específico. El monto en disputa
        no puede exceder el monto del pago.
        Para simular una disputa en la zona de pruebas, consulte
        "Simulating Cardholder Disputes".

        El objeto disputa contiene los siguientes campos:

            + token. "string": Id del objeto "Dispute". Cadena
                    que comienza con "dispute".

            + amount. "number": Importe del pago, en unidades definidas
                    por "currency". Decimal, incluido el número
                    correcto de lugares decimales para el exponente de
                    la moneda, tal como se define en la norma
                    ISO 2417:2015. Si la cantidad es un número entero,
                    use un número entero y no un decimal.

            + central_processing_date. "string": La fecha en que la
                    transacción fue procesada por el sistema de
                    tarjeta.

            + created_at. "number": Hora de creación de esta disputa.
                    en tiempo Unix. Solo respuesta.

            + currency. "string": Define la moneda de transacción. Sino se
                    especifica, la moneda oficial principal del país.
                    Código ISO 4217 de tres letras.

            + disoute_category. "string": La categoria de la disputa
                    proporcionada por el sistema de tarjetas.

            + dispute_reason_description. "string": Una breve descripción
                    opcional del motivo de la disputa.

            + due_date. "string": La última fecha para disputar la disputa
                    en tiempo Unix. Solo respuesta.

            + ewallet_id. "string": ID de la billetera en la que se ingresa
                    el dinero. Cadena que comienza con "ewallet" . Relevante
                    cuando la solicitud incluye una sola billetera.
                    Solo respuesta.

            + fixed_side "string": Indica si la tasa de cambio es fija para
                    el lado de la compra o para el lado de la venta.
                    Relevante para devoluciones con divisas. Solo respuesta.

            + is_refutable. "boolean": Indica si el pago puede ser
                    reembolsado.

            + is_reversal. "boolean": Indica si el pago se puede revertir.

            + metadata. "object": Un objeto JSON definido por el cliente.

            + original_dispute_amount. "number": Monto del pago en disputa,
                    en unidades definidas por "curerncy". Decimal, incluido
                    el número correcto de lugares decimales para el exponente
                    de la moneda, tal como se define en la norma ISO 2417:2015.

            + original_dispute_currency. "string": Moneda del pago en disputa.
                    Código ISO 4217 de tres letras. Mayúsculas.

            + original_transaction_amount. "number": Monto de la transacción
                    que se disputa, incluidas las tarifas brutas de transacción
                    en unidades definidas por "currency". Decimal, incluido el
                    número correcto de lugares decimales para el exponente de
                    la moneda, tal como se define en la norma ISO 2417:2015.

            + original_transaction_id. "string": Id del objeto de pago contra
                    el que se acredita la disputa. Cadena que comienza con
                    "payment".

            + payment_method. "object": Incluye datos del método de pago que
                    se utilizó para el pago. Consulte "Payment Method Data
                    Object".

            + rate. "number": Tipo de cambio relevante para metodos de pago FX.

            + reversal. "string": Reservado.

            + status. "string": Indica el estado de la operación de disputa.
                    Uno de los siguientes valores:
                        * ACT (Activo)
                        * RVW (Revisar)
                        * LOS (Perdido) - Estado final.
                        * WIN (Ganar) - Estado final.

            + updated_at. "number": Hora en que se actualizó por última vez
                    esta disputa, en tiempo Unix. Solo respuesta.

    """

    token = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2,
                                 blank=True, null=True)
    central_processing_date = models.CharField(max_length=20,
                                               null=True,
                                               blank=True)
    created_at = models.BigIntegerField(null=True, blank=True)
    currency = models.CharField(max_length=3, null=True, blank=True)
    dispute_category = models.CharField(max_length=20,
                                        null=True, blank=True)
    dispute_reason_descrption = models.CharField(max_length=20,
                                                 null=True,
                                                 blank=True)
    due_date = models.CharField(max_length=20,
                                null=True,
                                blank=True)
    ewallet_id = models.CharField(max_length=40,
                                  null=True,
                                  blank=True)
    fixed_side = models.CharField(max_length=5,
                                  null=True,
                                  blank=True)
    is_refundable = models.BooleanField(null=True, blank=True)
    is_reversal = models.BooleanField(null=True, blank=True)
    metadata = models.JSONField(null=True, blank=True)  # Json Object
    original_dispute_currency = models.CharField(max_length=3,
                                                 null=True,
                                                 blank=True)
    original_transaction_amount = models.DecimalField(max_digits=10,
                                                      decimal_places=2,
                                                      null=True, blank=True)
    original_transaction_currency = models.CharField(max_length=3,
                                                     null=True, blank=True)
    original_transaction_id = models.CharField(max_length=50,
                                               null=True,
                                               blank=True)
    payment_method = models.JSONField(null=True, blank=True)
    rate = models.IntegerField(null=True, blank=True)
    reversal = models.CharField(max_length=10, null=True, blank=True)
    status = models.CharField(max_length=3, null=True, blank=True)
    updated_at = models.BigIntegerField(null=True, blank=True)
