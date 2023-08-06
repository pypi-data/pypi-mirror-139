from rest_framework.test import APITestCase
from ..utilities import make_request
from ..serializers import GroupPaymentSerializer, PaymentSerializer
from ..models.group_payment import GroupPayment
from ..models.payment import Payment


class GroupPaymentTest(APITestCase):

    def test_create(self):

        # Creamos un grupo de pago con dos diferentes pagos
        body = {

                "payments":
                [{
                    "capture": "false",
                    "amount": "2.4",
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
                    },
                    {
                    "capture": "false",
                    "amount": "8",
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
                }]
            }

        # Enviamos la peticion a rapyd para crear el grupo
        response = make_request(
                method="post",
                path="/v1/payments/group_payments", body=body
                )
        # guardamos el pago en la base
        serializer = GroupPaymentSerializer(data=response['data'])

        if serializer.is_valid():
            serializer.save()
        else:
            print("Group", serializer.errors)

        # Validamos que el id que guardamos sea el mismo que nos envio rapyd
        idDb = GroupPayment.objects.last()
        self.assertEqual(idDb.id, response['data']['id'])

    def test_refund(self):

        # Creamos un grupo de pago con pagos que tengan el status closed
        body = {
                "payments":
                [{
                    "amount": "2.4",
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
                    },
                    {
                    "amount": "8",
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
                }]
            }

        # Enviamos la peticion a rapyd para crear el grupo
        response = make_request(
                method="post",
                path="/v1/payments/group_payments", body=body
                )
        # Tomamos los datos de la respuesta y los guardamos en la base
        serializer = GroupPaymentSerializer(data=response['data'])

        if serializer.is_valid():
            serializer.save()
        else:
            print("Group", serializer.errors)

        # Creamos un body con el id del grupo del pago creado
        body2 = {
            "group_payment": response['data']['id']
        }

        # Se envia la peticion a rapyd indicando de que
        # grupo queremos hacer un refund
        response = make_request(
            method="post",
            path="/v1/refunds/group_payments", body=body2
            )

        # Tomamos los datos de la respuesta y los guardamos en la base
        groupUpdate = GroupPayment.objects.get(id=body2["group_payment"])
        serializer = GroupPaymentSerializer(
            instance=groupUpdate, data=response['data'])

        if serializer.is_valid():
            serializer.save()
        else:
            print("Goup", serializer.errors)

        # Se toman los datos de cada pago individual
        # enviados en la respuesta de rapyd y los guardamos en la base
        for payments in response['data']['payments']:
            paymentSerializer = PaymentSerializer(data=payments)
            if paymentSerializer.is_valid():
                paymentSerializer.save()
            else:
                print("payment", paymentSerializer.errors)

        # Validamos que el estado refunded de los pagos sea igual a true
        idDb = Payment.objects.last()
        self.assertEqual(True, idDb.refunded)

    def test_retrieve(self):

        id = "gp_b9b400853d94cd14a72a9f7aee7148bb"
        response = make_request(
            method="get",
            path=f'/v1/payments/group_payments/{id}'
            )

        self.assertEqual(
            'gp_b9b400853d94cd14a72a9f7aee7148bb', response['data']['id'])
