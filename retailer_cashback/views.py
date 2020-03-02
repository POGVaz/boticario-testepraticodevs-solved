from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.contrib.auth import authenticate

from retailer_cashback import models, serializers, services

import logging
logger = logging.getLogger(__name__)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_retailer(request):
    request_data = {
        'email': request.POST.get('email'),
        'password': request.POST.get('password'),
        'first_name': request.POST.get('first_name'),
        'last_name': request.POST.get('last_name'),
        'cpf': request.POST.get('cpf'),
    }

    created_retailer = services.create_retailer(**request_data)
    logger.info("Created new retailer {}".format(created_retailer.user.username))
    return Response("Registered {}".format(created_retailer.user.username))

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def validate_retailer(request):
    user = authenticate(username=request.GET.get('username'),
                        password=request.GET.get('password'))

    if user is not None:
        return Response("User {} is Valid".format(user.username))
    else:
        logger.info("User {} is Invalid".format(
            request.GET.get('username')))
        response = Response("User {} is Invalid".format(
            request.GET.get('username')))
        response.status_code = status.HTTP_400_BAD_REQUEST
        return response

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_purchase(request):
    request_data = {
        'code': request.POST.get('code'),
        'purchase_date': request.POST.get('date'),
        'cpf': request.POST.get('cpf'),
        'value': request.POST.get('value'),
    }
    # Creates a purchase with all the business logic required
    purchase = services.create_purchase(**request_data)
    return Response("Purchase registered: {}".format(purchase.code))

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_purchases(request):
    queryset = models.Purchase.objects.order_by('-code')
    serializer = serializers.PurchaseSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def accumulated_cashback(request):
    return Response(services.get_accumulated_cashback(request.GET['cpf']))
