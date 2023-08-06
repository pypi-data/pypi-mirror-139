from django.db import models
from .payment import Payment


class Refund(models.Model):

    """El objeto Reembolso describe un único reembolso que se acredita
        contra un objeto Pago específico. Puede crear un reembolso cuando
        se cierra el pago. No hay límite en el número de reembolsos y el
        monto puede exceder el monto del pago. El dinero se devuelve al
        método de pago que se utilizó para realizar el pago.

        Para reembolsar un pago en el que los fondos se cobran a partir de
        dos o más métodos de pago, consulte "Create Group Refund".

        * El objeto reembolso contiene los siguientes campos:

            + id "string": Id del objeto reembolso. Cadena que comienza
                    con "refund".

            + amount. "number": Monto del reembolso, en unidades definidas
                    por "currency". Decimal, incluido el número
                    correcto de lugares decimales para el exponente de
                    la moneda, tal como se define en la norma
                    ISO 2417:2015. Si la cantidad es un número entero,
                    use un número entero y no un decimal.  Si se omite este
                    parámetro en la solicitud 'Crear reembolso', el
                    reembolso es por el monto total restante del objeto
                    'pago'. Para obtener más información, consulte
                    "Create Refund Request Parameters".

            + balance_transaction. "string": La cantidad no reembolsada que
                    queda en el pago. Solo respuesta.

            + created_at. "string": Hora de creación del reembolso en tiempo
                    Unix. Solo respuesta.

            + currency. "string": Código ISO 4217 de tres letras para la
                    moneda utilizada en el parámetro. Solo Respuesta.

            + ewallets. "array of objects": Una matriz de uno o más objetos
                    que representan billeteras a las que se carga el reembolso.
                    Cada objeto contiene los siguientes campos:

                        * id - El ID de la billetera, una cadena que comienza
                                con "ewallet". Requerido.
                        * amount - El monto del reembolso cargado a esta
                                billetera. Decimal. Necesario cuando no se
                                utiliza "percentage".
                        * percent - El porcentaje del reembolso cargado a esta
                                billetera. Decimal entre 0 y 100. Obligatorio
                                cuando no se utiliza "amount".

                    Nota: Todas las carteras deben especificar "amount" o todas
                    las carteras deben especificar "percentaage".
                    Para obtener más información, consulte
                    "Create Refund Request Parameters".

            + failure_reason. "string": Indica el motivo por el que falló el
                    reembolso. Uno de los siguientes:
                        * Lost_or_stolen_card
                        * expired_or_canceled_card
                        * unknown

            + fx_rate. "string": Tipo de cambio de la transacción. Cuando
                    "fixed_side" es "buy" , es la tasa de compra. Cuando es
                    "sell", es la tasa de venta. Número decimal como cadena.
                    Relevante para devoluciones con divisas. Solo respuesta.

            + merchant_reference_id. "string": Identificación definida por el
                    comerciante. Limitado a 255 caracteres.

            + metadata. "object": Un objeto JSON definido por el cliente.

            + merchant_debited_amount. "string": Monto debitado del
                comerciante. Relevante para devoluciones con divisas.
                Solo respuesta.

            + merchant_debited_currency. "string": Indica la moneda que se
                    debita del comercio. Código ISO 4217 de tres letras.
                    Relevante para devoluciones con divisas. Solo respuesta.

            + payment. "string": Id del objeto de pago contra el que se
                    acredita el reembolso. Cadena que comienza con "payment".

            + payment_created_at. "number": Hora en que se creó el pago
                    original en tiempo Unix. Solo respuesta.

            + payment_method_type. "string": El tipo de método de pago de
                    pago original. Use Listar métodos de pago por país
                    para obtener una lista de los tipos admitidos para
                    un país.

            + proportional_refund: "boolean": Indica si el reembolso fue
                    devuelto en proporción a los montos recibidos por los
                    monederos en el pago. Relevante para un reembolso por un
                    pago dividido entre varias billeteras.

            + reason. "string": Descripcion del motivo del reembolso,
                    proporcionada por el comerciante.

            + receipt_number: "string": Número del recibo de la devolución,
                    proporcionado por el comercio. Solo respuesta.

            + status. Indica el estado de la operación de devolución. Uno de
                    los siguientes valores: "Completed" : el reembolso se
                    completó. "Rejected" : el reembolso no se realizó debido
                    a un error interno. "Pending" : la solicitud creó un
                    objeto de reembolso en la plataforma Rapyd, pero el
                    reembolso aún no se ha completado. Por ejemplo, el
                    reembolso es para un método de pago que requiere una
                    acción del cliente, como efectivo, redireccionamiento
                    bancario o transferencia bancaria. Solo lectura.

            + updated_at. "number". Hora en que se actualizó por ultima vez
                    este reembolso en horario Unix. Solo respuesta.

    """

    id = models.CharField(primary_key=True, max_length=40)
    amount = models.DecimalField(max_digits=10, decimal_places=2,
                                 blank=True, null=True)
    balance_transaction = models.CharField(max_length=10, null=True,
                                           blank=True)
    create_at = models.BigIntegerField(blank=True, null=True)  # Unix time
    currency = models.CharField(max_length=3, blank=True, null=True)
    ewallets = models.TextField(null=True, blank=True)  # Array
    failure_reason = models.CharField(max_length=20, blank=True, null=True)
    fixed_side = models.CharField(max_length=5, null=True,
                                  blank=True)
    fx_rate = models.CharField(max_length=20, null=True,
                               blank=True)
    merchant_reference_id = models.CharField(max_length=255,
                                             blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)
    merchant_debited_amount = models.CharField(max_length=10, null=True,
                                               blank=True)
    merchant_debited_currency = models.CharField(max_length=3, null=True,
                                                 blank=True)
    payment_created_at = models.BigIntegerField(blank=True, null=True)
    payment_method_type = models.CharField(max_length=20,
                                           blank=True, null=True)
    proportional_refund = models.BooleanField(null=True, blank=True)
    reason = models.CharField(max_length=40, blank=True, null=True)
    receipt_number = models.CharField(max_length=10, null=True, blank=True)
    status = models.CharField(max_length=10, blank=True, null=True)
    updated_at = models.BigIntegerField(blank=True, null=True)

    # Referencia a Refund
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
