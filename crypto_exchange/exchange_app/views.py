from django.shortcuts import render
from exchange_app.models import Condition
from django.http import JsonResponse, HttpResponse
from .serializers import ConditionSerializer, UsersSerializer
from .models import Condition, Users, Wallets

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status 

# Create your views here.
def test(request): 
    results = Condition.objects.all().values('time', 'value')

    data = list (results)
    return JsonResponse(data, safe=False)

@api_view (['GET'])
def get_time_value(request): 
    # results = Condition.objects.all().values('time', 'value')
    results = Condition.objects.all()
    serialized_data =ConditionSerializer(results, many=True)
    return JsonResponse(list(results), safe = False) 
    # return Response(results)
# @api_view(['GET'])
# def get_users(request): 
#     results = Users.objects.all().values('first_name', 'username')
#     return JsonResponse(list(results), safe=False)


@api_view(['GET'])
def get_users(request): 
    results = Users.objects.all()
    serializer = UsersSerializer(results, many=True) 
    # print(UsersSerializer(Users.objects.all(), many=True).data)
    return Response(serializer.data) 


@api_view(['POST'])
def deposit(request):
    user_id = request.data.get('user_id')
    currency = request.data.get('currency')
    amount = request.data.get('amount')

    if not user_id or not currency or not amount:
        return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = Users.objects.get(id=user_id)
    except Users.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    try:
        wallet = Wallets.objects.get(user=user, currency=currency)
        created = False
    except Wallets.DoesNotExist:
        wallet = Wallets.objects.create(user=user, currency=currency, balance=0)
        created = True

    wallet.balance += amount
    wallet.save()

    if created:
        return Response({'message': f'Wallet created and {amount} {currency} deposited'}, status=status.HTTP_201_CREATED)
    else:
        return Response({'message': f'Successfully deposited {amount} {currency}'}, status=status.HTTP_200_OK)