from django.shortcuts import render
from exchange_app.models import Condition
from django.http import JsonResponse, HttpResponse
from .serializers import ConditionSerializer, UsersSerializer, WalletsSerializer, OrdersSerializer
from .models import Condition, Users, Wallets, Orders 

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status 

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate,  get_user_model
from django.contrib.auth.hashers import check_password
import json 
# Create your views here.
def test(request): 
    results = Condition.objects.all().values('time', 'value')

    data = list (results)
    return JsonResponse(data, safe=False)

@api_view (['GET'])
def get_time_value(request): 
  
    results = Condition.objects.all()
    serialized_data =ConditionSerializer(results, many=True)
    return JsonResponse(list(results), safe = False) 
  

@api_view(['GET'])
def get_users(request): 
    results = Users.objects.all()
    serializer = UsersSerializer(results, many=True) 
    return Response(serializer.data) 

@api_view(['GET'])
def get_wallets_currency(request, currency, user_id): 
    if not Wallets.objects.filter(user_id=user_id).exists(): 
        return Response({"error": "There is no such user_id"}, status=status.HTTP_404_NOT_FOUND)
    if not Wallets.objects.filter(user_id=user_id, currency=currency).exists(): 
        return Response({"error": "There is no such currency for this user"}, status=status.HTTP_404_NOT_FOUND)
    
    results = Wallets.objects.get(currency=currency, user_id=user_id)
    
    
    serializer = WalletsSerializer(results)
    
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
    

@api_view(['POST'])
def logout (request): 
    gmail = request.data.get('gmail')
    username = request.data.get('username')
    results = Users.objects.filter(username=username, email=gmail)
    login = False
    for value in results: 
        jwt = value.jwt_tokens
        if jwt: 
            jwt_dict = json.loads(jwt) 
            if(jwt_dict.get('access_token')): 
                login = True
                break 
    

    if login: 
        Users.objects.filter(username=username, email=gmail).update(jwt_tokens=json.dumps({}))
        return Response({"message": f"Successfully log out {username} {gmail}"}, status=status.HTTP_200_OK)
    else: 
        return Response({"error": "Such user not loggined"}, status= status.HTTP_404_NOT_FOUND)
@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')


    
    User = get_user_model()

    try:
        
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = None
    next = False 
    if (user.password == password):
        next = True 
    
    if user and next:
        
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        
        user.jwt_tokens = json.dumps({
            'access_token': access_token,
            'refresh_token': refresh_token
        })
        user.save()

        return Response({
            'access': access_token,
            'refresh': refresh_token,
        })
    else:
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    
@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        serializer = UsersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def place_order(request): 
    username = request.data.get('username')
    type = request.data.get('type')
    price = request.data.get('price')
    quantity = request.data.get('quantity')
    coin = request.data.get('coin')
    user = Users.objects.get(username=username)
    orders = Orders.objects.create(user = user, type = type, price = price, quantity = quantity, coin = coin)
    orders.save()
    return HttpResponse(f'<h1>{orders}</h1>')
    return HttpResponse(f'<h1>{type}</h1>\n<h1>{price}</h1>\n<h1>{quantity}</h1>\n<h1>{coin}</h1>')
    #validation in this process 
    
    
@api_view(['GET'])
def orders (request): 
    orders = Orders.objects.all()
    serializer = OrdersSerializer(orders, many=True) 
    return Response(serializer.data) 
@api_view(['GET'])
def specific_order(request, order_id): 
    order = Orders.objects.get(id = order_id)
    serializer = OrdersSerializer(order) 
    return Response(serializer.data) 

@api_view(['GET'])
def cancel_order(request, order_id): 
    try: 
        order = Orders.objects.get(id=order_id)
    except: 
        return Response({"error":"No Such order_id exist"}, status=status.HTTP_404_NOT_FOUND)
    order.delete()
    return Response({"message": f"Successfully delete order"}, status=status.HTTP_200_OK)
