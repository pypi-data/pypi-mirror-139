from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..utilities import make_request


# ******Serializers*******
from collect.serializers import DisputeSerializer

# *******Models***********
from ..models.dispute import Dispute

# Create your views here.


@api_view(['GET'])
def listDispute(request, limit):

    response = make_request(
        method="get",
        path=f'/v1/disputes?limit={limit}'
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


@api_view(['GET'])
def retrieveDispute(request, id):

    response = make_request(
        method="get",
        path=f'/v1/disputes/{id}'
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


# Obtener pago de la DB
@api_view(['GET'])
def getBdDispute(request):

    if request.user.has_perm('collect.can_view_dispute'):
        dispute = Dispute.objects.all()
        serializer = DisputeSerializer(dispute,
                                       many=True)
        return Response(serializer.data)
    else:
        print("No tiene permiso")
        return HttpResponse(
            f'{request.user} No tiene permiso de ver las disputas')
