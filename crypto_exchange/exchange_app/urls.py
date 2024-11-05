from django.urls import path, re_path
from exchange_app import views

urlpatterns = [
    path('conditions/', views.test, name='conditions'),
    path('api/get_time_value/', views.get_time_value, name='get_time_value'),
    path('api/get_users/', views.get_users, name='get_users'), 
    #need to make it after api/deposit/user_id
    path('api/wallets/deposit/', views.deposit, name='deposit'), 
    path ('api/wallets/withdraw/<int:user_id>/', views.withdraw_currency, name="withdraw_currency"),
    path('api/wallets/<int:user_id>/', views.get_wallets_currency, name="get_wallets_currency"), 
    path ('api/wallets/<int:user_id>/', views.get_all_wallets_currencies, name="get_all_wallets_currencies"), 
    path('api/login', views.login, name='login'), 
    path('api/register/', views.register, name='register'), 
    path('api/logout', views.logout, name='logout')
]
