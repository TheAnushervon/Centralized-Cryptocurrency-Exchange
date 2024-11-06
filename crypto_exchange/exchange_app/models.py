from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, username, password, **extra_fields)

class Users(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=256, unique=True)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    password = models.CharField(max_length=256)
    # kyc_details = models.JSONField()
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    jwt_tokens = models.JSONField(default=dict)  # This will store tokens in JSON format
    last_login = models.DateTimeField(null=True, blank=True)
    is_superuser = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'users'




# Create your models here.
class Condition(models.Model):
    time = models.DateTimeField()
    sensor_id = models.IntegerField()
    value = models.FloatField(null=True)
    id = models.IntegerField(primary_key=True)
    class Meta: 
        db_table = 'conditions'

# class Users(models.Model): 
#     id = models.AutoField(primary_key=True)
#     username= models.CharField(max_length=256)
#     email=models.CharField(max_length=256)
#     password = models.CharField(max_length=256)
#     first_name = models.CharField(max_length=256)
#     last_name = models.CharField(max_length=256)
#     kyc_details = models.JSONField()
#     class Meta: 
#         db_table = 'users'

class Wallets (models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='user_id', default =1)
    currency = models.CharField(max_length=20)
    balance = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: 
        db_table = "wallets"

class Orders(models.Model):
    BUY = 'buy'
    SELL = 'sell'
    ORDER_TYPES = [
        (BUY, 'Buy'),
        (SELL, 'Sell'),
    ]
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='user_id')
    type = models.CharField(max_length=4, choices=ORDER_TYPES)
    price = models.DecimalField(max_digits=18, decimal_places=6)  # Price per unit
    quantity = models.DecimalField(max_digits=18, decimal_places=6)  # Quantity of crypto
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, default='open')  # e.g., open, completed, cancelled
    coin = models.CharField(max_length=10)
    def __str__(self):
        return f"{self.type.capitalize()} Order: {self.quantity} at {self.price}"
    class Meta: 
        db_table = "orders"
        