from django.shortcuts import render
from exchange_app.models import Condition
from django.http import JsonResponse, HttpResponse
from .serializers import ConditionSerializer, UsersSerializer, WalletsSerializer, OrdersSerializer
from .models import Condition, Users, Wallets, Orders, Verification
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status 

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate,  get_user_model
from django.contrib.auth.hashers import check_password
import json 

from django.conf import settings 
from django.core.mail import send_mail
from .tasks import match_orders
import random

from .orderbook import OrderBook, Order
from django.db.models import F,Case, When, Value, IntegerField
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
  
@api_view (['GET'])
# @permission_classes([IsAuthenticated])
def get_user(request): 
    try:
        user = request.user  # The authenticated user is attached to the request
        print(f"user:{user}")
        return Response({
            "firstname": user.first_name,
            "lastname": user.last_name,
            "email": user.email,
            "id": user.id, 
        })
    except Exception as e:
        return Response({"error": "Failed to fetch user details."}, status=500)
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
def get_all_wallets_currencies(request):
    try: 
        user = request.user        
        results = Wallets.objects.filter(user_id=user.id)
        print("RESULTS: ", results) 
        if results.exists(): 
            serialized = WalletsSerializer(results, many=True)
            return Response(serialized.data) 
        else:     
            return Response({"error": "There is no such user_id"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": "Failed to fetch user details."}, status=500)
@api_view(['POST'])
def withdraw_currency(request):
    user = request.user 
    print("HERE USER: ", user)
    if not Wallets.objects.filter(user_id=user.id).exists(): 
        return Response({"error": "There is no such user_id exists"}, status=status.HTTP_404_NOT_FOUND)
    currency = request.data.get('currency')
    amount_want = request.data.get('amount')
    wallet = Wallets.objects.get(user_id=user.id, currency=currency)
    if (wallet.balance < amount_want): 
        return Response({"error": "You can not withdraw such amount of currency"}, status=status.HTTP_409_CONFLICT)
    wallet.balance -=amount_want
    wallet.save() 
    return Response({"message": "Withdrawal successful", "new_balance": wallet.balance, "currency": wallet.currency}, status=status.HTTP_200_OK)
@api_view(['POST'])
def deposit(request):
    # user_id = request.data.get('user_id')
    user = request.user
    currency = request.data.get('currency')
    amount = request.data.get('amount')

    if  not currency or not amount:
        return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = Users.objects.get(id=user.id)
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
    email = request.data.get('email')
    password = request.data.get('password')

    
    print(f"Email: {email}")
    print(f"Password: {password}")
    
    

    try:
        
        user = Users.objects.get(email = email)
        print("USER " , user) 
    except Users.DoesNotExist:
        user = None
    next = False 
    if (user.password == password):
        next = True 
    
    if user and next:
        
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        
        user.jwt_tokens = {
            'access_token': access_token,
            'refresh_token': refresh_token
        }
        user.save()

        return Response({
            'access': access_token,
            'refresh': refresh_token,
        })
    else:
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    
@api_view(['POST'])
def register(request):
    firstname = request.data.get("first_name")
    lastname = request.data.get("last_name")
    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")

    # Create the user
    # user = Users.objects.create_user(first_name = firstname, last_name = lastname, username=username, email=email, password=password)

    # Generate a 6-digit code and save it to VerificationCode model
    code = str(random.randint(100000, 999999))
    Verification.objects.create(email = email, code=code)
    # ISSUE 
    # CURRENT ISSUE IS THAT FOR OTHER EMAILS EXCEPT anushervon4j is not sending password
    # Send the code via email
    send_mail(
        "Your Verification Code",
        f"Your verification code is {code}.",
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )

    return Response({"message": "Verification code sent to your email"}, status=201)
@api_view(['POST'])
def verify_register(request):
    firstname = request.data.get("first_name")
    lastname = request.data.get("last_name")
    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")
    code = request.data.get('code')
    print(f"First Name: {firstname}")
    print(f"Last Name: {lastname}")
    print(f"Username: {username}")
    print(f"Email: {email}")
    print(f"Password: {password}")
    print(f"Code: {code}")
    try: 
        verification = Verification.objects.get(email=email, code = code)
    except Verification.DoesNotExist: 
        return Response({"message": "Invalid verification code"}, status=status.HTTP_400_BAD_REQUEST)
    
    user = Users.objects.create(first_name=firstname, last_name=lastname, username=username, email=email, password=password)
    verification.delete()
    return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def place_order(request): 
    user = request.user
    # username = request.data.get('username')
    type = request.data.get('type')
    price = request.data.get('price')
    quantity = request.data.get('qty')
    coin = request.data.get('coin')
    # type = user.type 
    # price = user.price
    # coin = user.coin 
    user = Users.objects.get(username=user.username)
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


ADMIN_USER_EMAIL = "anushervon4j@gmail.com"

def send_test_mail(request):
    try:
        send_mail(
            "Testing sending mail", 
            "Should work now!", 
            settings.EMAIL_HOST_USER,  
            [ADMIN_USER_EMAIL], 
            fail_silently=False, 
        )
        return HttpResponse("<h1>Success!</h1>")
    except Exception as e:  
        return HttpResponse(f"<h1>Error: {e}</h1>")

@api_view(['POST'])
def trigger_match_orders(request): 
    try: 
        match_orders.delay()
        return JsonResponse({'status': 'Task sent to Celery worker'})
    except e: 
        return JsonResponse({'status': 'Invalid request method'}, status=400)
    

order_book = OrderBook()

@api_view(['POST'])
def match(request):
    from django.db.models import F, Case, When, Value
    from django.db.models.fields import CharField

    pending_orders = Orders.objects.filter(status="open").order_by("created_at")

    for db_order in pending_orders:
        order = Order(
            order_id=db_order.id,
            symbol=db_order.coin,
            order_type=db_order.type,
            price=float(db_order.price),
            quantity=float(db_order.quantity),
            timestamp=db_order.created_at.timestamp(),
        )
        order_book.add_order(order)

    matched_orders = order_book.match_orders()

    for match in matched_orders:
        try:
            buy_order = Orders.objects.get(id=match['buy_order_id'])
            sell_order = Orders.objects.get(id=match['sell_order_id'])
        except Orders.DoesNotExist:
            continue

        buy_order.quantity = F('quantity') - match['quantity']
        sell_order.quantity = F('quantity') - match['quantity']

        buy_order.status = Case(
            When(quantity__lte=0, then=Value('completed')),
            default=Value('open'),
            output_field=CharField(),
        )
        sell_order.status = Case(
            When(quantity__lte=0, then=Value('completed')),
            default=Value('open'),
            output_field=CharField(),
        )

        buy_order.save()
        sell_order.save()
        
    Orders.objects.filter(status="completed").delete()
    Orders.objects.filter(quantity=0).delete()

    return Response({"matched_orders": matched_orders}, status=200)