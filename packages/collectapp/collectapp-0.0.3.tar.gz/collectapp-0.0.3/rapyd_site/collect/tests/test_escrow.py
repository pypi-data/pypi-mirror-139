from rest_framework.test import APITestCase
from ..utilities import make_request


class EscrowTest(APITestCase):

    def test_release(self):
        # Se crea un pago indicando que tiene escrow y la duracion
        # en dias

        body = {
            "amount": "22.4",
            "currency": "MXN",
            "payment_method": {
                "type": "mx_visacredit_card",
                "fields": {
                        "number": "4111111111111111",
                        "expiration_month": "10",
                        "expiration_year": "23",
                        "cvv": "123",
                        "name": "Manuel con visa mx"
                }
            },
            "escrow": "true",
            "escrow_release_days": "5"
        }

        # Se hace la peticion a rapyd para crear el pago
        response1 = make_request(
                method="post",
                path="/v1/payments", body=body
                )
        # Tomamos el id del escrow obtenido en la respuesta del pago
        payment = response1['data']['id']
        escrow = response1['data']['escrow']['id']

        # Con el id del escrow y pago se hace la peticion a rapyd para liberar
        # el escrow
        response = make_request(
            method="post",
            path=f"/v1/payments/{payment}/escrows/{escrow}/escrow_releases",
            body=body
            )

        # Validamos que el estatus cambio a released
        self.assertEqual(response['data']['status'], 'released')

    def test_list(self):
        # Con el id de pago y escrow obtenemos los datos del escrow
        payment = "payment_2602eb084ae4358a00a5cfff9672df06"
        escrow = "escrow_e8caefa27bc73d35e9a6d1e4b11a9f23"
        response = make_request(
            method="get",
            path=f'/v1/payments/{payment}/escrows/{escrow}/escrow_releases'
            )
        # Validamos que el id del escrow liberado sea igual al que esperamos
        self.assertEqual(
            'er_01cfdc11c71749ba7ec9dafa084a0521', response['data'][0]['id'])

    def test_retrieve(self):
        # Con el id de pago y escrow obtenemos los datos del escrow
        payment = "payment_2602eb084ae4358a00a5cfff9672df06"
        escrow = 'escrow_e8caefa27bc73d35e9a6d1e4b11a9f23'
        response = make_request(
            method="get",
            path=f'/v1/payments/{payment}/escrows/{escrow}'
            )

        self.assertEqual('released', response['data']['status'])
