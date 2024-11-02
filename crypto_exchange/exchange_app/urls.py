from django.urls import path, re_path
from exchange_app import views

urlpatterns = [
    path('conditions/', views.test, name='conditions'),
    path('get_time_value/', views.get_time_value, name='get_time_value'),
    path('get_users/', views.get_users, name='get_users')
]
