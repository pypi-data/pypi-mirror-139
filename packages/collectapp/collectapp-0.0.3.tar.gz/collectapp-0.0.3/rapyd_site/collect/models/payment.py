from django.db import models
from .group_payment import GroupPayment
from .outcome import Outcome
from .paymentFees import PaymentFee
from .client_details import ClientDetail
from .escrow import Escrow
from .dispute import Dispute
from .payment_method_data import PaymentMethodData
from .customer import Customer


class Payment(models.Model):

    """Un pago recopila fondos de una fuente (llamada método de pago)
        y los deposita en una o más billeteras Rapyd.
        Todo el proceso se gestiona con métodos en el objeto Pago.

        * Atributos:
            + id. "string" ID del pago. Cadena que comienza con "payment".
                   Solo respuesta.

            + address. "object": Dirección de facturación asociada
                        con un pago específico.

            + amount. "number": La cantidad recibida por el destinatario,
                    en unidades de la moneda definida en "currency". Decimal,
                    incluido el número correcto de lugares decimales para el
                    exponente de la moneda, tal como se define en la norma ISO
                    2417:2015.
                    Para verificar una tarjeta, configure en 0.

            + cancel_reason. "string": Motivo de la cancelación o de un pago.

            + capture. "boolean": Determina cuándo se procesa el pago para su
                    captura. Relevante para pagos con tarjeta.
                        - Verdadero : captura el pago inmediatamente. Este es
                                el valor predeterminado.
                        - Falso : autorice el pago, luego capture una parte
                                o la totalidad del pago en un momento
                                posterior, cuando el comerciante ejecute
                                el método de captura de pago .

                        Nota: Algunos métodos de pago con tarjeta no admiten la
                                captura diferida.

            + captured. "boolean": Indica si el pago se ha capturado
                    correctamente
            + client_details. "object": Información sobre el navegador del
                    cliente. Consulte Client Details Object.

            + complete_payment_url. "string": URL donde se redirige al cliente
                    para los pasos finales para completar la operación.
                    Proporcionado por el cliente.

                    Relevante para los métodos de pago de redirección bancaria.

            + country_code. "string": País del metodo de pago. Código ISO
                    3166-1 ALPHA-2 de dos letras. Solo respuesta.

            + created_at. "string": Hora de creación del pago en tiempo UNIX.

            + currency. "string": Define la moneda por la cantidad recibida por
                    el vendedor (comerciante). Código ISO 4217 de tres letras.

                    En las transacciones de FX, cuando "fixed_side" es "buy",
                    es la moneda recibida por el comerciante. Cuando es "sell",
                    es la moneda cargada al comprador. Véase también los campos
                    "fixed_side"y "requested_currency".
                    Este valor se refleja en el campo "currency_code" de la
                    respuesta.

            + currency_code. "string": Indica la moneda del importe recibido
                    por el destinatario. Código ISO 4217 de tres letras.
                    Solo respuesta.

            + customer. "string": Id  del cliente que está realizando el pago.
                    Cadena que comienza con "cus". Obligatorio si
                    "payment_method" está en blanco. Para obtener más
                    información, consulte "Customer object".

            + customer_token. "string". Id del cliente que está realizando el
                    pago. Cadena que comienza con "cus" . Cuando se crea un
                    pago sin un cliente existente, la plataforma crea un
                    cliente anónimo sin métodos de pago. Solo lectura.
                    Para obtener más información, consulte "Customer object".

            + destination_card. "string": Id de la tarjeta de destino para
                    la que es el pago. Relevante para pagos "card to card".

            + description. "string": Descripción de la transacción de pago.

            + dispute. "object": Detalles sobre la disputa, si el pago fue
                    disputado. Solo respuesta.

            + ending_before. "string": El Id del pago creado después del
                    último pago que desea recuperar. Cadena que comienza
                    con "pago".

            + error_code. "string": Mensaje de error relevante
                    (con un guión bajo entre palabras) y número de
                    identificación del error. Solo respuesta.

            + error_message. "string": Reservado.

            + error_payment_url. "string": URL donde se redirige al cliente
                    en caso de error en la operación. Proporcionado por el
                    cliente.
                    Relevante para los métodos de pago de redirección bancaria.

            + escrow. "boolean". Determina si el pago se mantiene en
                    deposito para su liberación posterior.

            + escrow. "object": Describe el depósito en garantía. Relevante
                    cuando el pago se crea con el valor true. Solo respuesta.
                    Consulte "Escrow object".

            + escrow_release_days. "number": Determina el número de días
                    después de la creación del pago que los fondos se
                    liberan del depósito en garantía. Los fondos se liberan
                    a las 5:00 p.m. GMT del día indicado. Entero, rango: 1-90.

            + ewallet_id. "string": ID de la billetera en la que se ingresa
                    el dinero. Cadena que comienza con "ewallet". Relevante
                    cuando la solicitud incluye una sola billetera.
                    Solo respuesta.

            + ewallets. "array of objects". Especifica las billeteras en las
                    que se recolecta el dinero. Si se deja en blanco, el dinero
                    va a la cartera del cliente de tipo "collection" más
                    antigua. Si no hay una billetera de cliente de
                    "collection", el dinero va a la billetera de cliente de
                    tipo "general" más antigua. Consulte "Wallets array" .

            + expiration."number": Fin del tiempo permitido para que el cliente
                    complete este pago, en tiempo Unix. El valor predeterminado
                    es 2 semanas. Relevante para  los métodos de pago donde
                    el campo "is_expirable" es verdadero en la respuesta a
                    "List Payment Methods By Country".

            + failure_code. "string": Código de error que explica el motivo
                    de la falta de pago.

            + failure_message. "string": Mensaje al comerciante, explicando el
                    motivo de la falta de pago. Solo respuesta.

            + fixed_side "string". Indica si el tipo de cambio es fijo para el
                    lado comprador (vendedor) o para el lado vendedor
                    (comprador).

                        - buy : la moneda que el vendedor (comerciante)
                                recibe por bienes o servicios.
                                La compra lateral fija se relaciona con los
                                fondos del vendedor (comerciante). Por ejemplo,
                                un comerciante con sede en EE. UU. quiere
                                cobrar 100 USD. El comprador (cliente) paga
                                el monto en MXN que se convierte en 100 USD.

                        - sell : la moneda con la que se carga al comprador
                                para comprar bienes o servicios al vendedor.
                                La venta lateral fija se relaciona con los
                                fondos del comprador (cliente). Por ejemplo,
                                un comerciante con sede en EE. UU. quiere
                                cobrarle a un comprador 2000 MXN y aceptará
                                cualquier monto en USD que se convierta de
                                2000 MXN.

            + flow_type. "string": Reservado.

            + fx_rate. "string": Tipo de cambio de la transacción. Cuando es
                    comprar , es la tasa de compra. Cuando se vende, es la tasa
                    de venta. Número decimal como cadena. Solo respuesta.

            + group. "boolean":Cuando es verdadero, incluye solo pagos
                    grupales en la respuesta. Cuando es falso, excluye
                    los pagos grupales de la respuesta. El valor
                    predeterminado es falso .

            + group_payment. "string": Id del pago del grupo. Cadena que
                    comienza con "gp". Relevante cuando el pago es parte de un
                    pago grupal.

            + id. "string": Id del pago. Cadena que comienta con "payment".
                    Solo respuesta.

            + initiation_type. "string": Indica cómo se inició la transacción.
                    Uno de los siguientes:
                        * customer_present : la transacción fue iniciada por el
                                cliente. Este es el valor predeterminado.
                        * installment - La transacción fue iniciada por una
                                suscripción donde hay un número fijo de cuotas.
                        * moto : la transacción se inició por pedido por correo
                                o por teléfono y fue iniciada por el
                                comerciante o el cliente de Rapyd.
                        * recurring : la transacción se inició mediante una
                                suscripción en la que los cargos se realizan a
                                intervalos regulares y no hay una fecha de
                                finalización.
                        * unscheduled : La transacción es una transacción de
                                recarga que fue previamente autorizada por el
                                titular de la tarjeta y fue iniciada por el
                                comercio o cliente Rapyd.

            + instructions. "object": Describe cómo el cliente realiza el pago.
                    Solo lectura. Contiene los siguientes campos:
                        * name. Descripción del método de pago.
                        * steps. Un objeto que contiene una lista de pasos que
                                debe seguir el cliente. Cada paso se denomina
                                paso N, donde N es un número entero.

            + invoice. "string": Id de la factura para la que se realiza el
                    pago. Cadena que comienza con "inv". Solo respuesta.

            + is_partial "boolean": Indica si el pago ha sido parcialmente
                    pagado. Cuando es falso, indica que el pago está pendiente
                    de pago o pagado en su totalidad. Solo respuesta.

            + limit. "string": El número máximo de pagos a devolver. Rango:
                    1-100. El valor predeterminado es 10.
                    Relevante para "List payments".

            + merchant_defined. "string": Reservado.

            + merchant_reference_id. "string": Id definido por el cliente.
                    Limitado a 255 caracteres.

            + merchant_requested_amount. "number": Indica el monto pagado
                    por el pagador, en unidades de la moneda definida en .
                    Relevante para pagos con FX. Solo lectura.

            + merchant_requested_currency."string": Indica la moneda que
                    recibe el comerciante. Código ISO 4217 de tres letras.
                    Mayúsculas. Relevante para pagos con FX. Solo respuesta.

            + metadata. "object": Objecto JSON definido por el cliente.

            + mid. "string": Reservado.

            + next_action. "string". Indica la siguiente acción para completar
                    el pago. Solo respuesta. Uno de los siguientes valores:
                        * 3d_verification : la siguiente acción es la
                                autenticación 3DS. Para simular la
                                autenticación 3DS en el espacio aislado,
                                consulte Simulación de la autenticación 3DS .
                                Relevante solo para pagos con tarjeta.
                        * pending_capture - La siguiente acción está pendiente
                                de la captura de la cantidad. Relevante solo
                                para pagos con tarjeta cuando el importe no
                                es cero.
                        * Pending_confirmation : la siguiente acción está
                                pendiente de la confirmación del pago.
                                Relevante para todos los métodos de pago
                                excepto el pago con tarjeta.
                        * not_applicable : el pago se completó o la siguiente
                                acción no es relevante.

            + order. "string" ID del pedido para el que es este pago.
                    Solo lectura. Relevante cuando el pago es por un pedido.

            + original_amount. "number":
                        * Foreign exchange payments: el monto pagado
                                por el remitente, en unidades de la moneda
                                definida en , incluidas las tarifas brutas de
                                transacción y las tarifas brutas de FX.
                        * Payments not involving foreign exchange: el monto
                                del pago, en unidades de la moneda definida
                                en, incluidas las tarifas de transacción
                                brutas.
                                Solo respuesta.

            + organization_id. "string": Reservado. Solo respuesta.

            + outcome. "object": Describe el resultado de la evaluación de
                    riesgos. Solo respuesta.

            + paid. "boolean": Indica si el pago se ha capturado por completo

            + paid_at. "numero". Hora de ultima captura en tiempo Unix.
                    Solo respuesta.

            + payment. "string":Id del pago. Cadena que comienda con "payment".

            + payment_fees. "object". Objeto que define las tarifas de
                    transacción y las tarifas de cambio de divisas.
                    Estas son tarifas que el comerciante Rapyd puede definir
                    para sus consumidores además del monto del pago. No están
                    relacionados con las tarifas que Rapyd cobra a
                    sus clientes.

                    Véase Payment fees object.

            + payment_method. "string u object": ID u objeto. Si no se
                    especifica en este campo, el método de pago es el método
                    de pago predeterminado especificado para el cliente.

                    Para obtener una descripción de los campos en el objeto,
                    consulte "Customer Payment Method Object".

            + payment_method_data: "object". Detalles del objeto
                    "payment_method_data". Consulte "Payment Method Data
                    Object". Solo respuesta.

            + payment_method_options. "object": Objeto que describe los
                    campos de método de pago adicionales requeridos para
                    el pago. Estos valores no se guardan como parte del
                    objeto de método de pago. Para determinar los campos
                    obligatorios, ejecute
                    "Get Payment Method Required Fields".

            + payment_method_type. "string": El tipo de metodo de pago. Para
                    obtener una lista de los tipos admitidos para un país
                    ejecute "List Payment Methods by Country".

            + payment_method_type_category. "string": Categoría del tipo de
                    método de pago. Solo lectura. Uno de los siguientes:
                        * bank_transfer
                        * bank_redirect
                        * card
                        * cash
                        * ewallet

            + receipt_email. "string": Dirección de correo electrónico a la
                    que se envía el recibo de esta transacción.

            + receipt_number "string": Reservado. Solo respuesta.

            + redirect_url. "string": URL donde se redirige al cliente para
                    los pasos adicionales necesarios para el pago.
                    Solo respuesta.

            + refunded. "boolean": Indica si hubo unreembolso contra este
                    pago. Solo respuesta.

            + refund_amount. "string": El monto total reembolsado contra
                    este pago, en unidades de la moneda definida en currency.
                    Solo respuesta.

            + refunded_amount. "number". El monto total reembolsado contra
                    este pago, en unidades de la moneda definida en currency.
                    Solo respuesta.

            + refunds. "object": Un objeto que contiene los siguientes campos:
                            * data - Una lista de hasta tres reembolsos.
                            * has_more - Indica si hay más de tres
                                    devoluciones contra este pago.
                            * total_count - Número total de devoluciones
                                    contra este pago.
                            * url - URL para solicitar todos los reembolsos
                                    de este pago. Solo respuesta.

            + remitter_information. "string": Contiene el nombre del cliente y
                    la cuenta bancaria asociada. Esto incluye:
                            * name. Nombre del cliente.
                            * account_id. ID de la cuenta bancaria del cliente.
                            * bank_code. Código SWIFT del banco del cliente.

                    Solo respuesta.

            + requested_currency. "string": Cuando "fixed_side" es "sell" ,
                    es la moneda recibida por el comerciante. Cuando es "buy"
                    , es la moneda que se le cobra al comprador (cliente)
                    para pagarle al vendedor (comerciante).
                    Código ISO 4217 de tres letras.
                    Relevante para pagos con FX.

            + show_intermediate_return_page. "boolean": La aplicación móvil
                    del comerciante redirige al cliente a la página web de
                    un banco para completar el pago. Cuando se completa el
                    pago, se redirige al cliente a una página de Pago
                    completo o de Error en la aplicación móvil. Si el banco
                    no admite la redirección de URL, establezca este campo
                    en verdadero y Rapyd enviará al banco una URL intermedia.
                    Una vez que se completa el pago, la URL intermedia de
                    Rapyd redirige al consumidor a la aplicación móvil.
                    El valor predeterminado es falso .

            + starting_after. "boolean": El ID del pago creado antes del primer
                    pago que desea recuperar. Cadena que comienza con "pago".

            + statment_descriptor. "string": Una descripción de texto adecuada
                    para el extracto de pago de un cliente. Limitado a 22
                    caracteres.

                    Si no se especifica este campo, Rapyd lo completa con el
                    nombre del comerciante.

            + status. "string": Indica el estado del pago. Solo respuesta.
                    Respuestas: una de las siguientes:
                        * ACT. activa y en espera de completar 3DS o capturar.
                                Se puede actualizar.
                        * CAN. Cancelado por el cliente o el banco del cliente.
                        * CLO. Cerrado y pagado.
                        * ERR. Error. Se intentó crear o completar un pago,
                                pero falló.
                        * EXP. El pago ha caducado.
                        * NEW. No cerrado.
                        * REV. Invertida por Rapyd.

            + textual_codes. "object": Un conjunto de códigos de texto para que
                    el cliente los use para completar los pasos descritos en el
                    campo. Solo respuesta. Contiene uno o más de los campos:

                        * code
                        * pay_code
                        * pairing_code
                        * payment_code
                        * response_code

            + token. "string": Id del pago a completar. Cadena que comienza con
                    "payment". Relevante para "Complete payment".

            + transaction_id "string". Id de la transacción asociada.

            + visual_codes. "object": Un conjunto de imágenes para que el
                    cliente las use para completar los pasos descritos en el
                    campo "instructions". Por ejemplo, un código QR o un
                    código de barras. Solo respuesta.

            + wallets. "array": Matriz de objetos que representan las
                    billeteras en las que se pagan los fondos.

    """

    id = models.CharField(primary_key=True, max_length=50)
    address = models.CharField(max_length=50, null=True,
                               blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True,
                                 blank=True)
    cancel_reason = models.CharField(max_length=40, null=True,
                                     blank=True)
    capture = models.BooleanField(default=True, null=True,
                                  blank=True)
    captured = models.BooleanField(null=True, blank=True)
    complete_payment_url = models.CharField(max_length=200, null=True,
                                            blank=True)
    country_code = models.CharField(max_length=2, null=True, blank=True)
    created_at = models.BigIntegerField(null=True,
                                        blank=True)  # Unix time
    currency = models.CharField(max_length=3, null=True,
                                blank=True)
    currency_code = models.CharField(max_length=3, null=True, blank=True)
    customer_token = models.CharField(max_length=50, null=True, blank=True)
    destination_card = models.CharField(max_length=40, null=True, blank=True)
    description = models.CharField(max_length=40, null=True, blank=True)
    ending_before = models.CharField(max_length=50, null=True, blank=True)
    error_code = models.CharField(max_length=40, null=True, blank=True)
    error_message = models.CharField(max_length=40, null=True, blank=True)
    error_payment_url = models.CharField(max_length=200, null=True, blank=True)
    escrow_release_days = models.IntegerField(null=True,
                                              blank=True)
    ewallet_id = models.CharField(max_length=50, null=True, blank=True)
    ewallets = models.TextField(null=True, blank=True)
    expiration = models.BigIntegerField(null=True,
                                        blank=True)  # Unix Time
    failure_code = models.CharField(max_length=40, null=True, blank=True)
    failure_message = models.CharField(max_length=40, null=True, blank=True)
    fixed_side = models.CharField(max_length=4, null=True, blank=True)
    flow_type = models.CharField(max_length=20, null=True, blank=True)
    fx_rate = models.CharField(max_length=5, null=True, blank=True)
    group = models.BooleanField(default=False, null=True, blank=True)
    initiation_type = models.CharField(max_length=20, null=True, blank=True)
    instructions = models.TextField(null=True, blank=True)
    invoice = models.CharField(max_length=50, null=True, blank=True)
    is_partial = models.BooleanField(null=True, blank=True)
    limit = models.CharField(max_length=3, null=True, blank=True)
    merchant_defined = models.CharField(max_length=20, null=True,
                                        blank=True)
    merchant_reference_id = models.CharField(max_length=255, null=True,
                                             blank=True)
    merchant_requested_amount = models.DecimalField(max_digits=10,
                                                    decimal_places=2,
                                                    null=True, blank=True)
    merchant_requested_curency = models.CharField(max_length=3, null=True,
                                                  blank=True)
    metadata = models.JSONField(null=True, blank=True)
    mid = models.CharField(max_length=3, null=True, blank=True)
    next_action = models.CharField(max_length=20, null=True, blank=True)
    orders = models.CharField(max_length=50, null=True, blank=True)
    original_amount = models.DecimalField(max_digits=10,
                                          decimal_places=2,
                                          null=True, blank=True)
    organization_id = models.CharField(max_length=5, null=True, blank=True)
    paid = models.BooleanField(null=True, blank=True)
    paid_at = models.BigIntegerField(null=True, blank=True)
    payment = models.CharField(max_length=50, null=True, blank=True)  # ?????
    payment_method = models.CharField(max_length=50, null=True,
                                      blank=True)
    payment_method_options = models.JSONField(null=True, blank=True)
    #
    payment_method_type_category = models.CharField(max_length=20, null=True,
                                                    blank=True)
    receipt_email = models.CharField(max_length=50, null=True,
                                     blank=True)
    receipt_number = models.CharField(max_length=20, null=True,
                                      blank=True)
    redirect_url = models.CharField(max_length=200, null=True,
                                    blank=True)
    refunded = models.BooleanField(null=True, blank=True)
    refund_amount = models.CharField(max_length=10, null=True, blank=True)
    refunded_amount = models.DecimalField(max_digits=10, decimal_places=2,
                                          null=True, blank=True)
    refunds = models.JSONField(null=True, blank=True)
    requested_currency = models.CharField(max_length=5, null=True,
                                          blank=True)
    show_intermediate_return_page = models.BooleanField(null=True,
                                                        blank=True)
    starting_after = models.CharField(max_length=5, null=True, blank=True)
    statement_descriptor = models.CharField(max_length=22, null=True,
                                            blank=True)
    status = models.CharField(max_length=3, null=True, blank=True)
    textual_codes = models.JSONField(null=True, blank=True)  # Object
    token = models.CharField(max_length=50, null=True,
                             blank=True)
    transaction_id = models.CharField(max_length=50, null=True,
                                      blank=True)
    visual_codes = models.JSONField(null=True, blank=True)  # Object
    wallets = models.CharField(max_length=10, null=True,
                               blank=True)  # Array

    # Payment method type no regresa Id
    # Referencia?????
    payment_method_type = models.CharField(max_length=50, null=True,
                                           blank=True)

    # Referencia a client detal
    client_details = models.ForeignKey(ClientDetail,
                                       on_delete=models.CASCADE,
                                       null=True, blank=True)

    # Referencia a customer
    customer = models.ForeignKey(Customer,
                                 on_delete=models.CASCADE,
                                 null=True, blank=True)

    # Referencia a Dispute

    dispute = models.ForeignKey(Dispute,
                                on_delete=models.CASCADE,
                                null=True, blank=True)

    # Referencia a escrow
    escrow = models.ForeignKey(Escrow, on_delete=models.CASCADE,
                               null=True, blank=True, related_name="escrow")
    # Referencia a group payment
    group_payment = models.ForeignKey(GroupPayment,
                                      on_delete=models.CASCADE,
                                      null=True,
                                      blank=True)

    # Ref a PaymentMethodData
    payment_method_data = models.ForeignKey(PaymentMethodData,
                                            on_delete=models.CASCADE,
                                            null=True,
                                            blank=True)

    # Ref a Outcome
    outcome = models.ForeignKey(Outcome,
                                on_delete=models.CASCADE,
                                null=True, blank=True)

    # Ref a Payment Fees
    payment_fees = models.ForeignKey(PaymentFee,
                                     on_delete=models.CASCADE,
                                     null=True, blank=True)
