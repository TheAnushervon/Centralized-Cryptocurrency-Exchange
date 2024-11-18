from django.urls import path, re_path
from exchange_app import views

urlpatterns = [
    path('conditions/', views.test, name='conditions'),
    path('api/get_time_value/', views.get_time_value, name='get_time_value'),
    path('api/get_users/', views.get_users, name='get_users'), 
    path('api/get_user/', views.get_user, name="get_user"), 
    #need to make it after api/deposit/user_id
    path('api/wallets/deposit/', views.deposit, name='deposit'), 
    path ('api/wallets/withdraw/', views.withdraw_currency, name="withdraw_currency"),
    path('api/wallets/<int:user_id>/<str:currency>', views.get_wallets_currency, name="get_wallets_currency"), 
    path ('api/wallets/', views.get_all_wallets_currencies, name="get_all_wallets_currencies"), 
    path('api/login', views.login, name='login'), 
    path('api/register/', views.register, name='register'), 
    path('api/verify_register/', views.verify_register, name = "verify_register"), 
    path('api/logout', views.logout, name='logout'), 
    path('api/orders/place', views.place_order, name = "place_order"), 
    path ('api/orders', views.orders, name = "orders"), 
    path ('api/orders/<int:order_id>/', views.specific_order, name = "specific_order"), 
    path('api/orders/<int:order_id>/cancel', views.cancel_order, name="cancel_order"), 
    path('api/trigger-match-orders', views.trigger_match_orders, name = "trigger_match_orders"), 
    path('api/match', views.match, name = "match"), 
    path('send_test_mail/', views.send_test_mail, name='send_test_mail'), 
]   
