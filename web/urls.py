from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='web_home'),
    path('register/', register, name='web_register'),
    path('login/', login, name='web_login'),
    path('logout/', logout, name='web_logout'),
    path('customer_dashboard/', customer_dashboard, name='web_customer_dashboard'),
    path('driver_dashboard/', driver_dashboard, name='web_driver_dashboard'),
    path('customer_delivery_transactions/', customer_delivery_transactions, name='web_customer_delivery_transactions'),
    path('driver_delivery_transactions/', driver_delivery_transactions, name='web_driver_delivery_transactions'),
    path('create_delivery_transaction/', create_delivery_transaction, name='web_create_delivery_transaction'),
    path('add_delivery_item/', add_delivery_item, name='web_add_delivery_item'),
    path('submit_delivery_transaction_request/', submit_delivery_transaction_request,
         name='web_submit_delivery_transaction_request')

]
