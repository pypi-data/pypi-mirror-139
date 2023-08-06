from rest_framework import status
from rest_framework.test import APITestCase
from ..utilities import make_request, test_request
from ..serializers import PaymentSerializer
from ..models.payment import Payment


class RefundTest(APITestCase):

    def test_create(self):
        # Pagos con estado CLO
        # Primero se crea un pago con estado clo

        body = {
            "amount": "5.2",
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
            }
        }
        # Se envia la peticion a rapyd para crear el pago
        response = make_request(
            method="post",
            path="/v1/payments", body=body
        )
        # Tomamos los datos de la respuesta y los guardamos en la base
        serializer = PaymentSerializer(data=response['data'])
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)

        # Creamos un body con el id de pago creado
        body2 = {
            "payment": response['data']['id']
        }

        # Se envia la peticion a rapyd con el id del
        # pago al que queremos hacer refund
        response = make_request(
            method="post",
            path="/v1/refunds", body=body2
        )
        # Al hacer el refund, rapy actualiza los datos del pago por lo que
        # se hace un get a ese pago para obtener sus datos actualizados
        paymentResponse = make_request(
            method="get",
            path=f"/v1/payments/{body2['payment']}"
        )

        # Actualizamos los datos del pago en la base
        paymentUpdate = Payment.objects.get(id=body2['payment'])
        paymentSerializer = PaymentSerializer(
            instance=paymentUpdate, data=paymentResponse['data'])

        if paymentSerializer.is_valid():
            paymentSerializer.save()
        else:
            print(paymentSerializer.errors)

        # Validamos que el estado refunded sea igual a True
        idDb = Payment.objects.last()
        self.assertEqual(idDb.refunded, True)

    def test_update(self):
        # Actualizar metadata en el refund

        # obtenemos el ultimo refund en rapyd
        list = make_request(
            method="get",
            path='/v1/refunds?limit=1'
        )

        # Aqui empieza el update

        # Se crea un body con el metadata actualizado
        body = {
            "metadata": {
                "merchant_defined": "updated"
            }
        }

        idUp = list['data'][0]['id']
        # Se envia el body con id del refund que queremos actualizar
        response = make_request(
            method="post",
            path=f"/v1/refunds/{idUp}",
            body=body
        )

        # Validamos que se actualizaron los datos del metadata
        self.assertEqual(
            "updated", response['data']['metadata']['merchant_defined'])

    def test_complete(self):

        body1 = {
            "amount": "6.8",
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
            }
        }
        # Se envia la peticion a rapyd para crear el pago
        response1 = make_request(
            method="post",
            path="/v1/payments", body=body1
        )

        # Creamos un body con el id de pago creado
        body2 = {
            "payment": response1['data']['id']
        }

        # Se envia la peticion a rapyd con el id del
        # pago al que queremos hacer refund
        response = make_request(
            method="post",
            path="/v1/refunds", body=body2)

        # Se crea un body con el metadata actualizado
        body3 = {
            "metadata": {
                "merchant_defined": "updated"
            }
        }

        # Se envia el body con id del refund que queremos actualizar
        make_request(
            method="post",
            path=f"/v1/refunds/{response['data']['id']}",
            body=body3
        )

        # Aqui comienza el complete
        # Obtenemos el id y lo ponemos en el body
        body = {
            "token": response['data']['id']
        }

        # Se envia la peticion a rapyd para completar el refund
        response = make_request(
            method="post",
            path="/v1/refunds/complete", body=body
        )

        # Validamos que el estado cambio a Completed
        self.assertEqual("Completed", response['data']['status'])

    def test_list(self):

        list = test_request(
            method="get",
            path='/v1/refunds?limit=3'
        )

        self.assertEqual(list.status_code, status.HTTP_200_OK)

    def test_retrieve(self):

        idUp = "refund_badc91ff0f35c079c82180e5ebf96a8c"
        response = make_request(
            method="get",
            path=f'/v1/refunds/{idUp}'
        )

        self.assertEqual(idUp, response['data']['id'])
