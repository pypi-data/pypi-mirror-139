from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..utilities import make_request


# ******Serializers*******
from collect.serializers import EscrowSerializer
from collect.serializers import PaymentSerializer, DisputeSerializer
from collect.serializers import PaymentMethodDataSerializer

# *******Models***********
from ..models.payment import Payment
from ..models.escrow import Escrow
from ..models.dispute import Dispute
from ..models.payment_method_data import PaymentMethodData

# Create your views here.


# ********Payments **************

# Create payment

@api_view(['POST'])
def createPayment(request):
    """

    Ejemplos de opciones de pago:

    Los datos se guardan en los modelos Escrow, Dispute
    PaymetnMethoData y sus llaves en Payment

    **Puedes ver los datos guardados mediante el admin**

    ****Poner uno de estos ejemplos dentro de
    content y darle en post: **


    pago con cash:

    {
        "amount": "16.1",
        "currency": "MXN",
        "payment_method": {
            "type": "mx_bancoazteca_cash"
        }
    }


    Pago con Escrow:
    **En el admin ver que se guardaron los datos en el
    modelo Escrow**

    {
        "amount" : "2.4",
        "currency" : "MXN",
        "payment_method" : {
            "type" : "mx_visacredit_card",
            "fields": {
                    "number" : "4111111111111111",
                "expiration_month" : "10",
                "expiration_year" : "23",
                "cvv" : "123",
                "name" : "Manuel con visa mx"
            }
        },
        "escrow" : true,
    "escrow_release_days" : "5"
        }




    Pago con Dispute, simular el pago con dispute en sandbox
    es con este numero de tarjeta en especifico:
    **En el admin ver que se guardaron los datos en el
    modelo Dispute**

    {
        "amount": 26.49,
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
        "capture" : true
    }




    Pagos con tarjeta capture=false para despues usar el
    capturePayment:

        {
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
    """
    body = request.data
    if request.user.has_perm('collect.can_add_payment'):
        response = make_request(
            method="post",
            path="/v1/payments", body=body)

        paymentMethodDataSerializer = PaymentMethodDataSerializer(
            data=response['data']['payment_method_data'])
        if paymentMethodDataSerializer.is_valid():
            paymentMethodDataSerializer.save()
        else:
            print("Payment Method Data", paymentMethodDataSerializer.errors)

        if "escrow" in body:
            escrowSerializer = EscrowSerializer(
                data=response['data']['escrow'])
            if escrowSerializer.is_valid():
                escrowSerializer.save()
            else:
                print("Escrow", escrowSerializer.errors)

        if response['data']['dispute']:
            disputeSerializer = DisputeSerializer(
                data=response['data']['dispute'])
            if disputeSerializer.is_valid():
                disputeSerializer.save()
            else:
                print("dispute", disputeSerializer.errors)

        serializer = PaymentSerializer(data=response['data'])

        if serializer.is_valid():
            serializer.save()

            payment = Payment.objects.get(id=response['data']['id'])

            payment.payment_method_data = PaymentMethodData.objects.get(
                id=response['data']['payment_method_data']['id'])
            payment.save()

            if 'escrow' in body:
                payment.escrow = Escrow.objects.get(
                    id=response['data']['escrow']['id'])
                payment.save()

            if response['data']['dispute']:
                payment.dispute = Dispute.objects.get(
                    token=response['data']['dispute']['token'])
                payment.save()
        else:
            print(serializer.errors)

        return Response(response["data"])

    else:
        return HttpResponse(
            f"{request.user} No tiene permisos de crear pagos")


@api_view(['POST'])
def updatePayment(request, id):
    """Pagos con status ACT que pueden ser pagos con cash,
       Pago con tarjetas con capture=false

       **En la URL poner el id del payment a actualizar**

       Se pueden actualizar datos del pago como
       receipt_email

       **En el admin puedes ver en Payment que se actulizaron
       los datos**
       Ejemplo

       {
           "receipt_email" : "actualizado@gmail.com"
       }

    """
    body = request.data
    payment = id
    if request.user.has_perm('collect.can_change_payment'):
        response = make_request(
            method="post",
            path=f"/v1/payments/{payment}", body=body
        )
        paymentUpdate = Payment.objects.get(id=payment)
        serializer = PaymentSerializer(
            instance=paymentUpdate, data=response['data'])

        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)

        return Response(response["data"])
    else:
        return HttpResponse(
            f"{request.user} No tiene permisos de actualizar")


@api_view(['POST'])
def capturePayment(request, id):
    """pagos de tarjeta con capture=false o status=Act

        **En la URL poner el id del payment a actualizar**

        El body puede ir vacio

        **En el admin puedes ver en Payment capture pasa a
        True**
    """

    body = request.data
    payment = id
    if request.user.has_perm('collect.can_change_payment'):
        response = make_request(
            method="post", path=f"/v1/payments/{payment}/capture",
            body=body)

        paymentCapture = Payment.objects.get(id=payment)
        serializer = PaymentSerializer(
            instance=paymentCapture, data=response['data'])

        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)

        return Response(response["data"])
    else:
        return HttpResponse(
            f"{request.user} No tiene permisos de capturar pagos")


@api_view(['POST'])
def completPayment(request):
    """Cambia el status a CLO en pagos en efectivo y
        operacion bancaria

        ejemplo:

        {

            "token" : "<id del payment a completar>"
        }
    """

    body = request.data
    if request.user.has_perm('collect.can_change_payment'):

        response = make_request(
            method="post", path="/v1/payments/completePayment", body=body)

        paymentCapture = Payment.objects.get(id=body['token'])
        serializer = PaymentSerializer(
            instance=paymentCapture, data=response['data'])

        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)

        return Response(response["data"])

    else:
        return HttpResponse(
            f"{request.user} No tiene permisos de completar pagos")


# Obtener pago de rapyd
@api_view(['GET'])
def retrievePayment(request, id):

    payment = id
    if request.user.has_perm('collect.can_view_payment'):
        response = make_request(
            method="get",
            path=f'/v1/payments/{payment}')

        return Response(response['data'])


# Obtener pago de rapyd
@api_view(['GET'])
def listPayment(request, limit):

    if request.user.has_perm('collect.can_view_payment'):
        response = make_request(
            method="get",
            path=f'/v1/payments?limit={limit}')

        return Response(response['data'])


# Cancelar Pag
@api_view(["DELETE"])
def cancelPayment(request, id):

    if request.user.has_perm('collect.can_delete_payment'):
        response = make_request(
            method="post", path=f"/v1/payments/{id}")

        paymentCancel = Payment.objects.get(id=id)
        serializer = PaymentSerializer(
            instance=paymentCancel, data=response['data'])

        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)

        return Response(response["data"])

    else:
        return HttpResponse(
            f"{request.user} No tiene permisos de completar pagos")


# Obtener pago de la DB
@api_view(['GET'])
def getBdPayments(request):

    if request.user.has_perm('collect.can_view_payment'):
        payment = Payment.objects.all()
        serializer = PaymentSerializer(payment,
                                       many=True
                                       )
        return Response(serializer.data)
    else:
        print("No tiene permiso")
        return HttpResponse(
            f'{request.user} No tiene permiso de ver los pagos')
