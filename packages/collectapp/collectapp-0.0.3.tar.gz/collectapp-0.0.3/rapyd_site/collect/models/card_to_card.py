from django.db import models
from .customer import Customer
from django_countries.fields import CountryField


class CardToCard(models.Model):

    """Los de tarjeta a tarjeta solo están disponibles para la categoría
        de método de pago "card_to_card".

        Permite el pago de fondos desde una tarjeta de origen a una
        tarjeta de destino.
        Los pagos de tarjeta a tarjeta incluyen estos pasos:

            1. Adjuntar los detalles de la tarjeta de origen a una
                    billetera Rapyd y tokenizarla.
                    "Consulte Add Source Card" .
            2. Creación de un pago desde la tarjeta de origen a la tarjeta
                    de destino. Consulte "Card to Card Payment".

        Requisitos previos:
            * Cliente. Consulte "Create Customer".

        * El objeto Card to Card contiene los siguientes campos:

            + id. "string": Id. del objeto de la página alojada.
                    Una cadena que comienza con "hpc2c_token" para agregar
                    la tarjeta de origen.
                    Una cadena que comienza con "hpc2c_transfer" para el pago
                    de tarjeta a tarjeta.
                    Solo respuesta.

            + billing_addess_collect. "boolean": Indica si la página alojada
                    muestra campos de dirección para completar.
                        * true : Se muestran los campos.
                        * false : Los campos se muestran solo para los códigos
                                de país de US, GB y CA. Este es el valor
                                predeterminado.

            + cancel_url. "string": URL donde se redirige al cliente después
                    de presionar Volver al sitio web para salir de la página
                    alojada. Esta URL anula la URL "merchant_website".

            + complete_payment_url. "string": URL donde se redirige al cliente
                    después de completar el pago con exito.

            + complete_url. "string": URL donde se redirige al cliente después
                    de presionar Cerrar para salir de la página alojada.
                    Esta URL anula la URL "merchant_website".

            + country. "string": El código ISO 3166-1 ALPHA-2 de dos letras del
                    país de la tarjeta de remitente.

            + currency. "string": Define la moneda de transacción. Sino se
                    especifica, la moneda oficial principal del país.
                    Código ISO 4217 de tres letras.

            + customer. "string": Id del cliente, una cadena que comienza
                    con "cus".
                    Para obtener mas información consulte "Customer Object".
                    Solo respuesta.

            + customer_addresses. "array of objects": Describe las direcciones
                    asociadas con este cliente.
                    Para obtener mas información consulte "Address Object".
                    Solo respuesta.

            + language. "string": Determina el idioma predeterminado de la
                    página alojada.
                    Los valores se enumeran en Compatibilidad con el idioma
                    de la página alojada .
                    Cuando este parámetro es nulo, se utiliza el idioma del
                    navegador del usuario.
                    Si no se puede determinar el idioma del navegador del
                    usuario, el idioma predeterminado es el inglés.

            + merchant_alias. "string": El nombre del cliente. El valor
                    predeterminado es "Rapyd".

            + merchant_color. "string": Color del botón de llamada a la acción
                    (CTA) en la página alojada. Solo respuesta.

                    Para configurar este campo, utilice el Portal del cliente.
                    Consulte Personalización de su página alojada .

            + merchan_customer_support "object": Datos de contacto de
                    atención al cliente, que contienen los siguientes campos:

                    * email. Dirección de correo electrónico.
                    * url. URL para el servicio de atención al cliente
                            del cliente.
                    * phone_number. Número de teléfono para contactar con el
                            servicio de atención al cliente del cliente.

                    Solo respuesta. Para configurar estos campos, utilice el
                    Portal del Cliente. "Customizing Your Hosted Page".

            + merchant_logo. "string": URL de la imagen del logo del cliente.
                    Solo respuesta.

            + merchant_website. "string": La URL a la que se redirige al
                    cliente después de salir de la página alojada.
                    Relevante cuando uno o ambos de los siguientes campos no
                    están configurados:

                        * cancel_url.
                        * complete_url.

                    Solo respuesta.
                    Para configurar este campo, utilice el
                    campo URL de respaldo en el Portal del cliente.

            + page_expiration. "number": Fin del tiempo en que el cliente
                    puede utilizar la página alojada, en tiempo Unix .
                    Si "page_expiration" no se establece, la página de pago
                    caduca 14 días después de la creación.
                    Rango: 1 minuto a 30 días.

            + payment_method. "string": Limita la página alojada a un tipo
                    específico de método de pago. Representa el token de la
                    tarjeta de pago. Cuando el cliente proporciona el
                    "payment_method", el pago de tarjeta a tarjeta en la
                    página alojada relacionada se limita a ese metodo de pago.
                    Puede seleccionar una tarjeta de origen
                    cuando "paymet_method" no se proporciona y el cliente
                    tiene varias tarjetas guardadas.

            + payment_method_type. "string": Limita la página a un tipo
                    específico de método de pago. Por ejemplo, dk_visa_card.
                    Para obtener una lista de métodos de pago, utilice
                    "List Payment Method by Country".

            + payment_params. "object": Reservado. Contiene los siguientes
                    campos:
                        * complete_payment_url
                        * error_payment_url.

                    Solo respuesta.

            + redirect_url. "string": URL de la pagina alojada. Solo respuesta.

            + status. "string": Estado de la pagina alojada. Uno de los
                    siguientes:
                        * NEW. La pagina fue creada.
                        * DONE. Se agregó una tarjeta.

                    Solo respuesta.

    """

    id = models.CharField(max_length=50, primary_key=True)
    billing_address_collect = models.BooleanField(null=True,
                                                  blank=True)
    cancel_url = models.CharField(max_length=80,
                                  null=True, blank=True)
    complete_payment_url = models.CharField(max_length=80,
                                            null=True, blank=True)
    complete_url = models.CharField(max_length=80,
                                    null=True, blank=True)
    country = CountryField(blank=True, null=True)
    currency = models.CharField(max_length=3, blank=True, null=True)
    customer_addresses = models.TextField(null=True, blank=True)
    language = models.CharField(max_length=20, null=True, blank=True)
    merchant_alias = models.CharField(max_length=20, null=True, blank=True)
    merchant_color = models.CharField(max_length=10, null=True, blank=True)
    merchant_customer_support = models.JSONField(null=True,
                                                 blank=True)  # Json type
    merchant_logo = models.CharField(max_length=80, null=True, blank=True)
    merchant_website = models.CharField(max_length=15, null=True, blank=True)
    page_expiration = models.BigIntegerField(null=True, blank=True)
    payment_method = models.CharField(max_length=20, null=True, blank=True)
    payment_method_type = models.CharField(max_length=20,
                                           blank=True, null=True)
    payment_method_params = models.JSONField(null=True,
                                             blank=True)     # Json type
    redirect_url = models.CharField(max_length=80, null=True, blank=True)
    status = models.CharField(max_length=5, null=True, blank=True)

    customer = models.ForeignKey(Customer,
                                 on_delete=models.CASCADE)
