from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..utilities import make_request


# ******Serializers*******
from collect.serializers import CardToCardSerializer
# *******Models***********

# Create your views here.


# ********Card to card **************

# Add source card
@api_view(['POST'])
def addSourceCard(request):

    body = request.data
    if request.user.has_perm('collect.can_add_card_to_card'):
        response = make_request(
            method="post",
            path="/v1/hosted/card_to_card/add_source_card",
            body=body
        )

        serializer = CardToCardSerializer(data=response['data'])

    else:
        return HttpResponse(
            f"{request.user} No tiene permisos de crear checkout")

    if serializer.is_valid():
        serializer.save()
    else:
        print(serializer.errors)

    return Response(response["data"])


# Obtener pago de rapyd
@api_view(['POST'])
def createCardToCardPayment(request, id):

    body = request.data

    if request.user.has_perm('collect.can_add_card_to_card'):
        response = make_request(
            method="post",
            path="/v1/hosted/card_to_card/transfer",
            body=body
        )

        serializer = CardToCardSerializer(data=response['data'])

    else:
        return HttpResponse(
            f"{request.user} No tiene permisos de crear checkout")

    if serializer.is_valid():
        serializer.save()
    else:
        print(serializer.errors)

    return Response(response["data"])
