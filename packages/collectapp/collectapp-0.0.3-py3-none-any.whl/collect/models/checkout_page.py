from django.db import models
# from .payment import Payment
from django_countries.fields import CountryField


class CheckoutPage(models.Model):

    """Una página de pago de Rapyd permite a un comerciante crear
        pagos para todos los métodos de pago disponibles. La página
        aparece directamente al cliente del comerciante. Puede
        configurarse como una página independiente o un i-frame dentro
        de la propia página web del cliente.

        Cuando el cliente envía una solicitud en la página,
        Rapyd le envía uno o más webhooks.

        Para obtener mas información consulte "Rapyd Checkout"

        * El objeto Página de pago contiene los siguientes campos:

            + id. "string": Id de la pagina de pago de Rapyd.
                    Cadena que comienza con "checkout".

            + amount. "number": El monto del pago, en unidades de la
                    moneda definida en "currency". Decimal, incluido
                    el número correcto de lugares decimales para el
                    exponente de la moneda, tal como se define en la
                    norma ISO 2417:2015. Si la cantidad es un número
                    entero, use un número entero y no un decimal.

            + checkout_cancel_url. "string": URL donde se redirige al
                    cliente después de presionar Volver al sitio web
                    para salir de la página alojada. Esta URL anula la
                    "merchant_website" URL. No es compatible con las
                    direcciones URL de localhost.

            + capture. "boolean": Determina cuándo se procesa el pago
                    para su captura. Relevante para pagos con tarjeta.

                    * true : captura el pago inmediatamente. Este es
                            el valor predeterminado.

                    * false : autorice el pago, luego capture una
                            parte o la totalidad del pago en un momento
                            posterior, cuando el comerciante ejecute
                            el método de captura de pago .

                    Nota: Algunos métodos de pago con tarjeta no admiten
                        la captura diferida.

            + cart_items. "array of objects": Describe los artículos del
                    carrito que el cliente está comprando. Estos artículos
                    se muestran en la página de pago. Contiene los siguientes
                    campos para cada artículo del carrito:

                    * name - El nombre del artículo. Requerido.
                    * amount- El precio del artículo en la moneda definida
                            en "currency "Requerido.
                    * quantity - La cantidad del artículo. Requerido.
                    * image - La imagen que aparece en la página de pago
                            de este artículo.

            + complete_checkout_url. "string": URL donde se redirige al
                    cliente después de presionar Finalizar para salir de la
                    página alojada. Esta URL anula la "merchant_website "URL.
                    No es compatible con las direcciones URL de localhost.

            + country. "string": El código de dos letras ISO 3166-1 ALPHA2
                    para el pais.

            + currency. "string": Define la moneda por la cantidad recibida
                    por el vendedor (comerciante). Código ISO 4217 de tres
                    letras.
                    En las transacciones de FX, cuando "fixed_side" es "buy",
                    es la moneda recibida por el comerciante. Cuando es "sell"
                    , es la moneda cargada al comprador.

            + ustom_elements. "object": Describe las personalizaciones de la
                    página tal como aparece al cliente. "Custom elements
                    objects".

            + customer."string": Id del cliente. Cadena que comienza con
                    "cus". Cuando se utiliza, el cliente tiene la opción de
                    guardar los datos de la tarjeta para futuras compras.
                    Este campo es obligatorio para ciertos métodos de pago del
                    modo de producción.

            + description. "string": Descripción de la transacción de pago.
                    Para mostrar la descripción, establezca "true" en
                    "display_description" .
                    Consulte Objeto de elementos personalizados.

            + error_payment_url: "string": URL a la que se redirige al cliente
                    después de que se produzca un error en el sitio de
                    terceros.
                    Relevante para los métodos de pago de redirección bancaria.
                    No es compatible con las direcciones URL de localhost.

            + escrow: "boolean": Determina si el pago se mantiene en
                    depósito para su liberación posterior.

            + escrow_releases_days. "number": Determina el número de
                    días después de la creación del pago que los fondos se
                    liberandel depósito en garantía. Los fondos se liberan a
                    las 5:00p. m. GMT del día indicado. Entero, rango: 1-90.

            + ewallet. "string": ID de la billetera en la que se ingresa el
                    dinero. Cadena que comienza con "ewallet".
                    Relevante para especificar una sola billetera en la
                    solicitud.

            + expiration. "number": Hora en que vence el pago si no se
                    completa en tiempo Unix . Cuando ambos "payment_expiration"
                    y "expiration" están configurados, el pago vence antes.
                    El valor predeterminado es 14 días después de la creación
                    de la página de pago.

            + fixed_side. "string": Indica si el tipo de cambio es fijo para
                    el lado comprador (vendedor) o para el lado vendedor
                    (comprador).
                    Uno de los siguientes valores:

                    * buy. la página de pago muestra la moneda que el vendedor
                            (comerciante) recibe por bienes o servicios. Este
                            es el valor predeterminado. Por ejemplo, un
                            comerciante con sede en EE. UU. quiere cobrar 100
                            USD. El comprador (cliente) paga el monto en MXN
                            que se convierte en 100 USD.
                    * sell. la página de pago muestra la moneda que se le
                            cobra al comprador para comprar bienes o servicios
                            al vendedor.Por ejemplo, un comerciante con sede en
                            EE. UU. quiere cobrarle a un comprador 2000 MXN y
                            aceptará cualquier monto en USD que se convierta de
                            2000 MXN.

            + language. "string": Determina el idioma predeterminado de la
                    página alojada. Los valores están documentados en
                    Compatibilidad con el idioma de la página alojada .
                    Cuando este parámetro es nulo, se utiliza el idioma del
                    navegador del usuario.
                    Si no se puede determinar el idioma del navegador del
                    usuario, el idioma predeterminado es el inglés.

            + merchant_alias. "string". Reservado. El valor predeterminado
                    es "Rapyd".

            + merchant_color. "string": Color del botón de acción en la
                    página alojada. Vea "Customizing Your Hosted Page".

            + merchant_customer_support. "object" Datos de contacto de atención
                    al cliente, que contienen los siguientes campos:

                    * email - Dirección de correo electrónico.
                    * url - URL para el servicio de atención al cliente del
                            cliente.
                    * phone_number - Número de teléfono para contactar con
                            el servicio de atención al cliente del cliente.

                    Solo respuesta.
                    Para configurar estos campos, utilice el Portal del
                    Cliente. Vea "Customizing Your Hosted Page".

            + merchant_logo "string": URL de la imagen del logo del cliente.
                    Solo respuesta. Vea "Customizing Your Hosted Page".

            + merchant_main_button. "string": Una cadena que representa
                    el texto del botón principal de llamada a la acción (CTA).
                    Uno de los siguientes:

                    * place_your_order - Realice su pedido. Este es el valor
                            predeterminado.
                    * pay_now - Pague ahora.
                    * make_payment - Realizar Pago.
                    * buy - Comprar.
                    * donate - Donar.

                    Solo respuesta. Vea "Customizing Your Hosted Page".

            + merchant_privacy_policy. "string": URL de la politica de
                    privacidad del cliente. Solo respuesta.
                    Vea "Customizing Your Hosted Page".

            + merchant_reference_id. "string": Identificador de la
                    transaccion. Definido por el comerciante. Puede ser
                    utilizado para la reconciliación.

            + merchant_terms. "string": URL de los terminos y condiciones
                    del cliente. Solo respuesta.
                    Vea "Customizing Your Hosted Page".

            + metadata. "object": Objeto JSON definido por el cliente.

            + page_expiration."number": Fin del tiempo en que el cliente
                    puede utilizar la página alojada, en tiempo Unix .
                    Si "page_expiration" no se establece , la página de pago
                    caduca 14 días después de la creación.
                    Rango: 1 minuto a 30 días.

            + payment. "object": Describe el pago que resultará de la página
                    alojada. Ver Objeto de Pago para más detalles. Los valores
                    "id" y "status" son nulos hasta que el cliente envía
                    correctamente la información en la página alojada.
                    Solo respuesta.

            + payment_expiration. "number": Periodo de tiempo que tarda
                    en completarse el pago después de que se crea, medido en
                    segundos. Cuando "page_expiration" y "expiration"
                    están configurados, el pago vence antes.

            + payment_fees. "object": Describe las tarifas que se pueden
                    cobrar por una transacción de pago.

            + payment_method. "Objeto que describe el método de pago.
                    Contiene los siguientes campos:

                    * type - El tipo de método de pago. Requerido.
                    * fields - Contiene los campos que son obligatorios para
                            el método de pago. Consulte Obtener campos
                            obligatorios del método de pago .
                    * name - Nombre del método de pago.
                    * address - Objeto 'Dirección' que describe la dirección
                            asociada con el pago. Consulte Objeto de dirección
                            . No utilice una ID de dirección.
                    * metadata - Objeto 'Metadatos' definido por el
                            comerciante. Consulte Objeto de metadatos .

                    Nota: este comportamiento es diferente de Crear pagos.

            + payment_method_type. "string": El tipo de método de pago.
                    Por ejemplo, it_visa_card .
                    Para obtener una lista de métodos de pago de un país,
                    utilice "List payment methods by country".

            + payment_method_type_categories. "array of strings": Una lista de
                    las categorías de métodos de pago que se admiten en la
                    páginade pago. Las categorías aparecen en la página en
                    el orden indicado. Uno o más de los siguientes:

                    * bank_redirect
                    * bank_transfer
                    * card
                    * cash
                    * ewallet

            + payment_method_types_excludes. "array of strings": Lista de
                    métodos de pago que están excluidos de la visualización
                    en la página de pago.

                    Consulte Configuración de la lista de métodos de pago .

            + payment_method_types_includes. "array of strings": Lista de
                    métodos de pago que se muestran en la página de pago.
                    Los métodos de pago aparecen en la página en el orden
                    proporcionado.

                    Consulte Configuración de la lista de métodos de pago .

            + redirect_url. "string": URL de la pagina de pago que se
                    muestra al cliente.

            + requested_currency "string": Cuando "fixed_side" es "sell", es
                    la moneda recibida por el comerciante. Cuando  es "buy",
                    es la moneda que se carga al comprador (cliente). La página
                    de pago muestra la siguiente información:
                    * El monto original y la moneda.
                    * El monto convertido en la moneda solicitada.
                    * El tipo de cambio. Código ISO 4217 de tres letras.
                    Relevante para pagos con FX.

            + status. "string": Indica el estado del pago. Uno de los
                    siguientes valores:
                    * NEW - Nuevo pago.
                    * ACT - Pago activo.
                    * CLO - Pago cerrado.

            + timestamp. "number": Hora de creación de la página de pago,
                    en tiempo Unix . Solo respuesta.

    """

    id = models.CharField(primary_key=True, max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2,
                                 null=True,
                                 blank=True)
    cancel_checkout_url = models.CharField(max_length=80,
                                           null=True,
                                           blank=True)
    capture = models.BooleanField(null=True, blank=True)
    cart_item = models.TextField(null=True, blank=True)
    complete_checkout_url = models.CharField(max_length=80,
                                             null=True,
                                             blank=True)
    complete_payment_url = models.CharField(max_length=80,
                                            null=True,
                                            blank=True)
    country = CountryField(null=True, blank=True)
    currency = models.CharField(max_length=3, null=True, blank=True)
    custom_elements = models.JSONField(null=True, blank=True)
    customer = models.CharField(max_length=50, null=True, blank=True)
    description = models.CharField(max_length=20, null=True, blank=True)
    error_payment_url = models.CharField(max_length=80, null=True, blank=True)
    escrow = models.BooleanField(null=True, blank=True)
    escrow_release_days = models.IntegerField(null=True, blank=True)
    ewallet = models.CharField(max_length=50, null=True, blank=True)
    ewallets = models.TextField(null=True, blank=True)
    expiration = models.BigIntegerField(null=True, blank=True)
    fixed_side = models.CharField(max_length=3, null=True, blank=True)
    language = models.CharField(max_length=20, null=True, blank=True)
    merchant_alias = models.CharField(max_length=20, null=True, blank=True)
    merchant_color = models.CharField(max_length=20, null=True, blank=True)
    merchant_customer_support = models.JSONField(null=True, blank=True)
    merchant_logo = models.CharField(max_length=80, null=True, blank=True)
    merchant_main_button = models.CharField(max_length=20,
                                            null=True,
                                            blank=True)
    merchant_privacy_policy = models.CharField(max_length=80,
                                               null=True,
                                               blank=True)
    merchant_reference_id = models.CharField(max_length=40,
                                             null=True,
                                             blank=True)
    merchant_terms = models.CharField(max_length=80, null=True, blank=True)
    merchan_website = models.CharField(max_length=80, null=True, blank=True)
    metadata = models.JSONField(null=True, blank=True)
    page_expiration = models.BigIntegerField(null=True, blank=True)
    payment_expiration = models.IntegerField(null=True, blank=True)
    payment_fees = models.JSONField(null=True, blank=True)
    payment_method = models.JSONField(null=True, blank=True)
    payment_method_type = models.CharField(max_length=20,
                                           null=True, blank=True)
    payment_method_type_categories = models.TextField(null=True, blank=True)
    payment_method_types_exclude = models.TextField(null=True, blank=True)
    payment_method_types_include = models.TextField(null=True, blank=True)
    redirect_url = models.CharField(max_length=200, null=True, blank=True)
    requested_currency = models.CharField(max_length=3, null=True, blank=True)
    status = models.CharField(max_length=3, null=True, blank=True)
    timestamp = models.BigIntegerField(null=True, blank=True)

    payment = models.JSONField(null=True, blank=True)

    # Se quito ref a payment ya que al crear el checkout, crea payment
    # sin id
    '''
    payment = models.ForeignKey(Payment,
                                on_delete=models.CASCADE,
                                null=True, blank=True)  # Referencia a Payment
    '''
