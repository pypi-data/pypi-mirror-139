from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..utilities import make_request


# ******Serializers*******
from collect.serializers import RefundSerializer, PaymentSerializer

# *******Models***********
from ..models.payment import Payment
from ..models.refund import Refund

# Create your views here.


# ********Refund **************

# Create prefund
@api_view(['POST'])
def createRefund(request):

    body = request.data
    payment = body['payment']
    if request.user.has_perm('collect.can_add_refund'):
        response = make_request(
            method="post",
            path="/v1/refunds", body=body
        )

        paymentResponse = make_request(
            method="get",
            path=f"/v1/payments/{payment}"
        )

        paymentUpdate = Payment.objects.get(id=payment)
        paymentSerializer = PaymentSerializer(
            instance=paymentUpdate, data=paymentResponse['data'])

        if paymentSerializer.is_valid():
            paymentSerializer.save()
        else:
            print(paymentSerializer.errors)

        serializer = RefundSerializer(data=response['data'])

        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)

        return Response(response["data"])

    else:
        return HttpResponse(
            f"{request.user} No tiene permisos de crear refunds")


@api_view(['POST'])
def updateRefund(request, id):
    """Cambiar el metadata
    """
    body = request.data
    refund = id

    if request.user.has_perm('collect.can_change_refund'):
        response = make_request(
            method="post",
            path=f"/v1/refunds/{refund}", body=body
        )
        refundUpdate = Refund.objects.get(id=refund)
        serializer = RefundSerializer(
            instance=refundUpdate,
            data=response['data'])

        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)

        return Response(response["data"])

    else:
        return HttpResponse(
            f"{request.user} No tiene permisos de actualizar")


@api_view(['POST'])
def completeRefund(request):

    body = request.data

    if request.user.has_perm('collect.can_change_refund'):
        """Pago hecho con efectivo o bancario y complete
        """
        response = make_request(
            method="post",
            path="/v1/refunds/complete", body=body)

        refundCapture = Refund.objects.get(id=body['token'])
        serializer = RefundSerializer(
            instance=refundCapture, data=response['data'])

        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)

        return Response(response["data"])

    else:
        return HttpResponse(
            f"{request.user} No tiene permisos de completar refunds")


@api_view(['GET'])
def listRefund(request, limit):

    response = make_request(
        method="get",
        path=f'/v1/refunds?limit={limit}'
    )
    return Response(response)

# Obtener pago de rapyd


@api_view(['GET'])
def retrieveRefund(request, id):

    refund = id
    response = make_request(
        method="get",
        path=f'/v1/refunds/{refund}'
    )

    return Response(response)


# Obtener pago de la DB
@api_view(['GET'])
def getBdRefunds(request):

    if request.user.has_perm('collect.can_view_refund'):
        refund = Refund.objects.all()
        serializer = RefundSerializer(refund,
                                      many=True)
        return Response(serializer.data)
    else:
        print("No tiene permiso")
        return HttpResponse(
            f'{request.user} No tiene permiso de ver los refunds')
