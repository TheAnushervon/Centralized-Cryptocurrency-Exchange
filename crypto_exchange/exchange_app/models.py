from django.db import models

# Create your models here.
class Condition(models.Model):
    time = models.DateTimeField()
    sensor_id = models.IntegerField()
    value = models.FloatField(null=True)
    id = models.IntegerField(primary_key=True)
    class Meta: 
        db_table = 'conditions'

class Users(models.Model): 
    id = models.AutoField(primary_key=True)
    username= models.CharField(max_length=256)
    email=models.CharField(max_length=256)
    password = models.CharField(max_length=256)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    kyc_details = models.JSONField()
    class Meta: 
        db_table = 'users'

class Wallets (models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='user_id', default =1)
    currency = models.CharField(max_length=20)
    balance = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: 
        db_table = "wallets"
