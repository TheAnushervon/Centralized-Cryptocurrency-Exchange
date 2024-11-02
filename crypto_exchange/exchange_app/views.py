from django.shortcuts import render
from exchange_app.models import Condition
from django.http import JsonResponse
from .serializers import ConditionSerializer, UsersSerializer
from .models import Condition, Users

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
    return Response(serializer.data) 
