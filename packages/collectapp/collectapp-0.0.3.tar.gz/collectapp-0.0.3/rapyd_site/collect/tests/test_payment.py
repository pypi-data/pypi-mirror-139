from rest_framework.test import APITestCase
from rest_framework import status
from ..utilities import make_request, test_request
from ..serializers import PaymentSerializer
from ..models.payment import Payment


class PaymentTest(APITestCase):

    def test_complete(self):
        # Pagos que tienen el estado ACT -> CLO
        # pagos en efectivo, banco, transferencia bancaria
        # Creamos un pago
        body1 = {
            "amount": "16.1",
            "currency": "MXN",
            "payment_method": {
                "type": "mx_bancoazteca_cash"
            }
        }

        # Se envia la peticion a Rapyd para crear el pago
        response1 = make_request(
            method="post",
            path="/v1/payments", body=body1
        )
        # Guardamos los datos en nuesta base de datos
        serializer1 = PaymentSerializer(data=response1['data'])
        if serializer1.is_valid():
            serializer1.save()
        else:
            print(serializer1.errors)

        # Aqui empieza el complete

        # Tomamos el id del pago en la respuesta de rapyd
        idUp = response1['data']['id']

        # Se asigna el id del pago que queremos completar en el body
        body = {
            "token": idUp
        }
        # Enviamos la peticion a rapyd de completar
        response = make_request(
            method="post",
            path="/v1/payments/completePayment",
            body=body
        )
        # Actualizamos los datos del pago en la base
        paymentCapture = Payment.objects.get(id=idUp)
        serializer = PaymentSerializer(
            instance=paymentCapture, data=response['data'])
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)

        # Verificamos que el estatus ahora sea CLO
        idDb = Payment.objects.get(id=idUp)
        self.assertEqual(idDb.status, 'CLO')

    def test_create(self):
        # Creacion de un pago, ejemplo para pago
        # con tarjeta sin customer asociado
        body = {
            "amount": "11.1",
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
            "capture": "false"
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

        # Verificamos que el pago se guardo correctamente
        # validando la cantidad del pago
        idDb = Payment.objects.get(id=response['data']['id'])
        self.assertEqual(float(idDb.amount), response['data']['amount'])

    def test_update(self):
        # Pagos que tengan el estado ACT se pueden
        # actualizar algunos campos, ej: email

        # Primero creamos un pag
        # Se toma el ultimo pago creado en rapyd para no hacer otro pago
        # ya que este contiene el estado ACT
        list = make_request(
            method="get",
            path='/v1/payments?limit=1'
        )
        # Tomamos los datos de la respuesta y los guardamos en la base
        for row in list["data"]:
            serializer = PaymentSerializer(data=row)
            if serializer.is_valid():
                serializer.save()
            else:
                print(serializer.errors)

        # Aqui empieza el update

        # Se agregan los campos a modificar
        body = {
            "receipt_email": "emailActualizado@gmail.com"
        }

        # Se envia la peticion a rapyd
        idUp = list['data'][0]['id']
        response = make_request(
            method="post",
            path=f"/v1/payments/{idUp}",
            body=body
        )
        # Actualizamos los datos del pago en la base
        paymentUpdate = Payment.objects.get(id=idUp)
        serializer = PaymentSerializer(
            instance=paymentUpdate, data=response['data'])
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)

        # Verificamos que el email se actualizo
        idDb = Payment.objects.get(id=idUp)
        self.assertEqual(idDb.receipt_email, 'emailActualizado@gmail.com')

    def test_capture(self):

        # pagos con tarjeta capture false -> true
        # Creamos un pago
        body1 = {
            "amount": "4.4",
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
            "capture": "false"
        }
        # Tomamos los datos de la respuesta y los guardamos en la base
        # Se envia la peticion a rapyd para crear el pago
        response1 = make_request(
            method="post",
            path="/v1/payments", body=body1
        )
        # Tomamos los datos de la respuesta y los guardamos en la base
        serializer = PaymentSerializer(data=response1['data'])
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)

        # Aqui empieza el capture

        # Tomamos el id del pago recibido
        idUp = response1['data']['id']

        # Enviamos la peticion a rapyd para capturar el pago
        response = make_request(
            method="post",
            path=f"/v1/payments/{idUp}/capture"
        )
        # Guardamos la respuesta en la base
        paymentCapture = Payment.objects.get(id=idUp)
        serializer = PaymentSerializer(
            instance=paymentCapture, data=response['data'])
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)

        # Verificamos que el estado capture se actualizo
        idDb = Payment.objects.get(id=idUp)
        self.assertEqual(idDb.captured, True)

    def test_list(self):
        response = test_request(
            method="get",
            path='/v1/payments?limit=5'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve(self):

        idPay = 'payment_e49c59f33ed7582cbd00587093ca02ad'
        response = test_request(
            method="get",
            path=f'/v1/payments/{idPay}'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
