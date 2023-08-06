from rest_framework.test import APITestCase
from ..utilities import make_request
from ..serializers import CheckoutSerializer
from ..models.checkout_page import CheckoutPage


class CheckoutTest(APITestCase):

    def test_create(self):
        # El checkout page es la pagina en donde observamos la
        # Cantidad a pagar y las opciones de pago que tenemos
        # Para crear un checkout page se envian los datos
        # del pago, amount, country y currency
        body = {
            "country": "MX",
            "currency": "MXN",
            "amount": 20
        }

        # Se envia la peticion a rapyd para crear un checkout page
        # con los datos enviados
        response = make_request(
            method="post",
            path="/v1/checkout", body=body
            )

        # Guardamos la respuesta en la base
        serializer = CheckoutSerializer(data=response['data'])

        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)

        # Validamos que el id que se obtuvo es el mismo que guardaos
        idDb = CheckoutPage.objects.last()

        self.assertEqual(idDb.id, response['data']['id'])

    def test_retrieve(self):
        # Obtenemos los datos de un checkout page creado
        id = "checkout_f67d6abae31f6fadd92ccc49b3170041"

        response = make_request(
            method="get",
            path=f'/v1/checkout/{id}'
            )

        self.assertEqual(20.00, response['data']['amount'])
