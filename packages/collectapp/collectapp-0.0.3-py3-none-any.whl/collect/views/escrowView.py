from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..utilities import make_request


# ******Serializers*******
from collect.serializers import EscrowSerializer

# *******Models***********
from ..models.escrow import Escrow

# Create your views here.


@api_view(['POST'])
def releaseEscrow(request, escrow, payment):

    body = request.data
    if request.user.has_perm('collect.can_add_escrow'):

        response = make_request(
            method="post",
            path=f"/v1/payments/{payment}/escrows/{escrow}/escrow_releases",
            body=body
        )
        escrowRelease = Escrow.objects.get(id=response['data']['id'])
        serializer = EscrowSerializer(
            instance=escrowRelease,
            data=response['data'])

    else:
        return HttpResponse(
            f"{request.user} No tiene permisos de libear escrows")

    if serializer.is_valid():
        serializer.save()
    else:
        print(serializer.errors)

    return Response(response["data"])


# Obtener pago de Rapyd
@api_view(['GET'])
def retrieveEscrow(request, escrow, payment):

    if request.user.has_perm('collect.can_view_escrow'):
        response = make_request(
            method="get",
            path=f'/v1/payments/{payment}/escrows/{escrow}'
        )

        '''
        for row in response["data"]:
        serializer = PaymentSerializer(data=row)

        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)
        '''
        return Response(response)
    else:
        return HttpResponse(
            f"{request.user} No tiene permisos de libear escrows")


@api_view(['GET'])
def listEscrow(request, escrow, payment):

    if request.user.has_perm('collect.can_view_escrow'):
        response = make_request(
            method="get",
            path=f'/v1/payments/{payment}/escrows/{escrow}/escrow_releases'
        )
        '''
        for row in response["data"]:
        serializer = PaymentSerializer(data=row)

        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)
        '''
        return Response(response)
    else:
        return HttpResponse(
            f"{request.user} No tiene permisos de libear escrows")


# Obtener pago de la DB
@api_view(['GET'])
def getBdEscrows(request):

    if request.user.has_perm('collect.can_view_payment'):
        escrow = Escrow.objects.all()
        serializer = EscrowSerializer(escrow,
                                      many=True)
        return Response(serializer.data)
    else:
        print("No tiene permiso")
        return HttpResponse(
            f'{request.user} No tiene permiso de ver los pagos')
