from django.shortcuts import render

from api.models import *


def home(request):
    if request.user.is_authenticated:
        context = {'welcome_message': f"Welcome, {request.user.username}!"}
    else:
        context = {'welcome_message': None}
    return render(request, 'home.html', context)


def register(request):
    gender_choices = PersonalInformation._meta.get_field('gender').choices
    user_type_choices = PersonalInformation._meta.get_field('user_type').choices
    context = {
        'gender_choices': gender_choices,
        'user_type_choices': user_type_choices,
    }
    return render(request, 'register.html', context)


def login(request):
    return render(request, 'login.html')


def logout(request):
    return render(request, 'logout.html')
