from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='web_home'),
    path('register/', register, name='web_register'),
    path('login/', login, name='web_login'),
    path('logout/', logout, name='web_logout'),
    path('customer_dashboard/', customer_dashboard, name='web_customer_dashboard'),
    path('driver_dashboard/', driver_dashboard, name='web_driver_dashboard'),
    path('delivery_transactions/', delivery_transactions, name='web_delivery_transactions'),
    path('create_delivery_transaction/', create_delivery_transaction, name='web_create_delivery_transaction'),
]
