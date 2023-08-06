from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..utilities import make_request

# ******Serializers*******
from collect.serializers import GroupPaymentSerializer
from collect.serializers import PaymentSerializer

# *******Models***********
from ..models.group_payment import GroupPayment
from ..models.payment import Payment

# Create your views here.


# ********Group Payments **************

# Crear pago en grupo
@api_view(['POST'])
def createGroupPayment(request):
    """Ejemplo para crear grupo de pagos

    Al crear un grupo de pago, en la tabla Payment, se agregan los
    pagos individuales con el id del grupo
    y en GroupPayment el grupo de pago



    {

    "payments":
            [{
                "capture" : true,
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
                }
            },
                {
                "capture" : true,
                "amount" : "8",
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
                }
            }]
    }


    """

    body = request.data
    if request.user.has_perm('collect.can_add_group_payment'):
        response = make_request(
            method="post",
            path="/v1/payments/group_payments", body=body
        )

        serializer = GroupPaymentSerializer(data=response['data'])

        if serializer.is_valid():
            serializer.save()
        else:
            print("Group", serializer.errors)

        for payments in response['data']['payments']:
            paymentSerializer = PaymentSerializer(data=payments)
            if paymentSerializer.is_valid():
                paymentSerializer.save()
            else:
                print("payment", paymentSerializer.errors)

        return Response(response["data"])
    else:
        return HttpResponse(
            f"{request.user} No tiene permisos de crear grupos de pagos")

# Crear reembolso de grupo


@api_view(['POST'])
def createGroupRefund(request):

    body = request.data

    if request.user.has_perm('collect.can_change_group_payment'):
        response = make_request(
            method="post",
            path="/v1/refunds/group_payments", body=body
        )
        groupUpdate = GroupPayment.objects.get(id=body["group_payment"])
        serializer = GroupPaymentSerializer(
            instance=groupUpdate, data=response['data'])

        if serializer.is_valid():
            serializer.save()
        else:
            print("Goup", serializer.errors)

        for payments in response['data']['payments']:
            paymentUpdate = Payment.objects.get(id=payments['id'])
            paymentSerializer = PaymentSerializer(
                instance=paymentUpdate, data=payments)
            if paymentSerializer.is_valid():
                paymentSerializer.save()
            else:
                print("payment", paymentSerializer.errors)

        return Response(response["data"])
    else:
        return HttpResponse(
            f"{request.user} No tiene permisos de actualizar")


# Obtener pago de rapyd
@api_view(['GET'])
def retrieveGroupPayment(request, id=None):

    if request.user.has_perm('collect.can_view_group_payment'):
        response = make_request(
            method="get",
            path=f'/v1/payments/group_payments/{id}'
        )

        return Response(response)


@api_view(['POST'])
# Cancel group payment
def cancelGroupPayment(request, id):

    body = request.data
    if request.user.has_perm('collect.can_delete_group_payment'):
        response = make_request(
            method="delete",
            path=f"/v1/payments/group_payments/{id}", body=body
        )
        groupUpdate = GroupPayment.objects.get(id=body["group_payment"])
        serializer = GroupPaymentSerializer(
            instance=groupUpdate, data=response['data'])

        if serializer.is_valid():
            serializer.save()
        else:
            print("Group", serializer.errors)

        for payments in response['data']['payments']:
            paymentUpdate = Payment.objects.get(id=payments['id'])
            paymentSerializer = PaymentSerializer(
                instance=paymentUpdate, data=payments)
            if paymentSerializer.is_valid():
                paymentSerializer.save()
            else:
                print("payment", paymentSerializer.errors)

        return Response(response["data"])

    else:
        return HttpResponse(f"{request.user} No tiene permisos de actualizar")


# Obtener group payment de la DB
@api_view(['GET'])
def getBdGroupPayment(request):

    if request.user.has_perm('collect.can_view_payment'):
        payment = GroupPayment.objects.all()
        serializer = GroupPaymentSerializer(payment,
                                            many=True)
        return Response(serializer.data)
    else:
        print("No tiene permiso")
        return HttpResponse(
            f'{request.user} No tiene permiso de ver los pagos')
