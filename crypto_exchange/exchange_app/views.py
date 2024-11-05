from django.shortcuts import render
from exchange_app.models import Condition
from django.http import JsonResponse, HttpResponse
from .serializers import ConditionSerializer, UsersSerializer, WalletsSerializer
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

@api_view(['GET'])
def get_wallets_currency(request, currency, user_id): 
    if not Wallets.objects.filter(user_id=user_id).exists(): 
        return Response({"error": "There is no such user_id"}, status=status.HTTP_404_NOT_FOUND)
    if not Wallets.objects.filter(user_id=user_id, currency=currency).exists(): 
        return Response({"error": "There is no such currency for this user"}, status=status.HTTP_404_NOT_FOUND)
    
    results = Wallets.objects.get(currency=currency, user_id=user_id)
    print(results) 
    print(results.balance)
    serializer = WalletsSerializer(results, many=True)
    print(serializer.data["created_at"])
    return Response(serializer.data) 

@api_view(['GET'])
def get_all_wallets_currencies(request, user_id): 
        results = Wallets.objects.filter(user_id=user_id)
        if results.exists(): 
            serialized = WalletsSerializer(results, many=True)
            return Response(serialized.data) 
        else:     
            return Response({"error": "There is no such user_id"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def withdraw_currency(request, user_id): 
    if not Wallets.objects.filter(user_id=user_id).exists(): 
        return Response({"error": "There is no such user_id exists"}, status=status.HTTP_404_NOT_FOUND)
    currency = request.data.get('currency')
    amount_want = request.data.get('amount')
    wallet = Wallets.objects.get(user_id=user_id, currency=currency)
    if (wallet.balance < amount_want): 
        return Response({"error": "You can not withdraw such amount of currency"}, status=status.HTTP_409_CONFLICT)
    wallet.balance -=amount_want
    wallet.save() 
    return Response({"message": "Withdrawal successful", "new_balance": wallet.balance, "currency": wallet.currency}, status=status.HTTP_200_OK)
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