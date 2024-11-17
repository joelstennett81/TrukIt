from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='api_register'),
    path('login/', LoginView.as_view(), name='api_login'),
    path('logout/', LogoutView.as_view(), name='api_logout'),
    path('driver_dashboard/', DriverDashboardView.as_view(), name='api_driver_dashboard'),
    path('customer_dashboard/', CustomerDashboardView.as_view(), name='api_customer_dashboard'),
    path('delivery_transaction/', CreateDeliveryTransactionView.as_view(), name='api_create_delivery_transaction'),
    path('add_delivery_item/', AddDeliveryItemView.as_view(), name='api_add_delivery_item'),
    path('get_delivery_cart_items/', GetDeliveryCartItemsView.as_view(), name='api_get_delivery_cart_items'),
]
