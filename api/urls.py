from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='api_register'),
    path('login/', LoginView.as_view(), name='api_login'),
    path('logout/', LogoutView.as_view(), name='api_logout'),
    path('driver_dashboard/', DriverDashboardView.as_view(), name='api_driver_dashboard'),
    path('customer_dashboard/', CustomerDashboardView.as_view(), name='api_customer_dashboard'),
    path('delivery_transaction/', DeliveryTransactionView.as_view(), name='api_delivery_transaction'),
]
