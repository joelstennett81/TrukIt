from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='web_home'),
    path('register/', register, name='web_register'),
    path('login/', login, name='web_login'),
    path('logout/', logout, name='web_logout')
]
