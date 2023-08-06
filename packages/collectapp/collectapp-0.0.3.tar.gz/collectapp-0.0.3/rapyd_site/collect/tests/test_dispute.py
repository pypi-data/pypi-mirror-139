from rest_framework import status
from rest_framework.test import APITestCase
from ..utilities import make_request, test_request


class EscrowTest(APITestCase):

    def test_retrieve(self):
        # Para tener una disputa creamos un pago con
        # un numero de tarjeta especifico otorgado por rapyd

        body = {
                "amount": 15.49,
                "currency": "USD",
                "merchant_reference_id": "first",
                "payment_method": {
                    "type": "fr_visa_card",
                    "fields": {
                        "number": "4539922288211219",
                        "expiration_month": "11",
                        "expiration_year": "23",
                        "cvv": "123",
                        "name": "John Doe"
                    }
                },
                "capture": "true"
              }
        # Se crea la peticion para hacer el pago
        response1 = make_request(
                method="post",
                path="/v1/payments", body=body
                )
        # Obtenemos el id de la disputa obtenido en los datos del pago
        dispute = response1['data']['dispute']['token']

        # Hacemos la peticion a rapyd para obtener los datos de la disputa
        response = make_request(
            method="get",
            path=f"/v1/disputes/{dispute}"
            )

        # Validamos que la disputa tenga la descripcion esperada
        self.assertEqual(
            response['data']['dispute_reason_description'],
            'Goods or Services Not Provided')

    def test_list(self):
        # Obtenemos el numero de disputas creadas
        response = test_request(
            method="get",
            path='/v1/disputes?limit=3'
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
