from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.hashers import make_password
import datetime


class RegisterView(APIView):
    def post(self, request):
        data = request.data
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        password = data.get('password')
        user_type = data.get('user_type')
        phone_number = data.get('phone_number')
        date_of_birth = data.get('date_of_birth')
        gender = data.get('gender')
        mailing_address = data.get('mailing_address')
        mailing_address_two = data.get('mailing_address_two')
        city = data.get('city')
        state = data.get('state')
        zip_code = data.get('zip_code')

        if User.objects.filter(username=email).exists():
            return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=email, email=email, password=password)
        print('user: ', user)
        personal_info = PersonalInformation.objects.create(
            user_id=user.id,
            first_name=first_name,
            last_name=last_name,
            email_address=email,
            phone_number=phone_number,
            date_of_birth=date_of_birth,
            gender=gender,
            mailing_address=mailing_address,
            mailing_address_two=mailing_address_two,
            city=city,
            state=state,
            zip_code=zip_code,
            password=make_password(password),
            user_type=user_type,
            registration_date=datetime.date.today()
        )

        if user_type == 'driver':
            Driver.objects.create(personal_information=personal_info)
        else:
            Customer.objects.create(personal_information=personal_info)

        login(request, user)

        return Response({'success': 'User registered successfully'}, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request):
        data = request.data
        email = data.get('email')
        password = data.get('password')
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return Response({'success': 'Logged in successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'success': 'Logged out successfully'}, status=status.HTTP_200_OK)
