from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..utilities import make_request

# ******Serializers*******
from collect.serializers import CheckoutSerializer

# *******Models***********
from ..models.checkout_page import CheckoutPage

# Create your views here.


# ********Checkou page **************

# Create checkout page
@api_view(['POST'])
def createCheckout(request):

    body = request.data
    if request.user.has_perm('collect.can_add_checkout_page'):
        response = make_request(
            method="post",
            path="/v1/checkout", body=body)

        serializer = CheckoutSerializer(data=response['data'])

    else:
        return HttpResponse(
            f"{request.user} No tiene permisos de crear checkout")

    if serializer.is_valid():
        serializer.save()
    else:
        print(serializer.errors)

    return Response(response["data"])


# Obtener pago de rapyd
@api_view(['GET'])
def retrieveCheckout(request, id):

    if request.user.has_perm('collect.can_view_checkout_page'):
        checkout = id
        response = make_request(
            method="get",
            path=f'/v1/checkout/{checkout}')
    return Response(response["data"])


# Obtener pago de la DB
@api_view(['GET'])
def getBdCheckout(request):

    if request.user.has_perm('collect.can_view_checkout_page'):
        checkout = CheckoutPage.objects.all()
        serializer = CheckoutSerializer(checkout, many=True)
        return Response(serializer.data)
    else:
        print("No tiene permiso")
        return HttpResponse(
            f'{request.user} No tiene permiso de ver los checkout')
