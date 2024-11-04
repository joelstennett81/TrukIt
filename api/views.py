from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .forms import *
from django.contrib.auth.hashers import make_password
import datetime

from .serializers import *


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
        city = data.get('city')
        state = data.get('state')
        zip_code = data.get('zip_code')

        if TrukItUser.objects.filter(email=email).exists():
            return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)

        new_user = TrukItUser.objects.create(
            username=email,
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            date_of_birth=date_of_birth,
            gender=gender,
            mailing_address=mailing_address,
            city=city,
            state=state,
            zip_code=zip_code,
            registration_date=datetime.date.today(),
            user_type=user_type
        )

        new_user.set_password(password)
        new_user.save()

        if user_type == 'driver':
            Driver.objects.create(truk_it_user=new_user)
        else:
            Customer.objects.create(truk_it_user=new_user)

        login(request, new_user)

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


class DriverDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        try:
            driver = Driver.objects.get(truk_it_user__user=user)
            insurance = DriverInsurance.objects.filter(driver=driver.truk_it_user)
            trailer = DriverTruckTrailer.objects.filter(driver=driver.truk_it_user)
            return Response({
                'driver_info': {
                    'first_name': driver.truk_it_user.first_name,
                    'last_name': driver.truk_it_user.last_name,
                    'email': driver.truk_it_user.email_address,
                    'phone_number': driver.truk_it_user.phone_number,
                    'insurance': list(insurance.values()),
                    'trailer': list(trailer.values())
                }
            }, status=status.HTTP_200_OK)
        except Driver.DoesNotExist:
            return Response({'error': 'Driver not found'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        user = request.user
        try:
            driver = Driver.objects.get(truk_it_user__user=user)
            data = request.data
            # Handle file uploads and other data processing here
            return Response({'success': 'Data uploaded successfully'}, status=status.HTTP_200_OK)
        except Driver.DoesNotExist:
            return Response({'error': 'Driver not found'}, status=status.HTTP_404_NOT_FOUND)


class CustomerDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        try:
            customer = Customer.objects.get(truk_it_user__user=user)
            return Response({
                'customer_info': {
                    'first_name': customer.truk_it_user.first_name,
                    'last_name': customer.truk_it_user.last_name,
                    'email': customer.truk_it_user.email_address,
                    'phone_number': customer.truk_it_user.phone_number,
                },
                'actions': {
                    'request_delivery': 'URL to request delivery'
                }
            }, status=status.HTTP_200_OK)
        except Customer.DoesNotExist:
            return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)


class DeliveryTransactionView(APIView):
    def post(self, request):
        try:
            delivery_transaction_data = request.data['transaction']
            delivery_item_data = request.data.get('item')

            if not delivery_transaction_data:
                return Response({'error': 'Transaction data is required'}, status=status.HTTP_400_BAD_REQUEST)

            transaction_serializer = DeliveryTransactionSerializer(data=delivery_transaction_data)
            if transaction_serializer.is_valid():
                transaction = transaction_serializer.save()

                if delivery_item_data:
                    item_serializer = DeliveryItemSerializer(data=delivery_item_data)
                    if item_serializer.is_valid():
                        item = item_serializer.save(transaction=transaction)
                        return Response({
                            'message': 'Delivery transaction and item created successfully',
                            'transaction_id': transaction.id,
                            'item_id': item.id
                        }, status=status.HTTP_201_CREATED)
                    else:
                        return Response(item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'message': 'No item data provided'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(transaction_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except KeyError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)