from rest_framework import serializers
from .models import Condition, Users, Wallets

class ConditionSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Condition
        fields = ["id", "time", "sensor_id", "value"]

class UsersSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Users
        fields = ["id", "username", "email", "password", "first_name", "last_name", "kyc_details"]

class WalletsSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Wallets 
        fields = ["id", "user_id", "currency", "balance", "created_at"]