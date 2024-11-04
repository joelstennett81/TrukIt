from django.shortcuts import render, redirect
from django.utils import timezone

from api.forms import *
from api.models import *


def home(request):
    if request.user.is_authenticated:
        context = {'welcome_message': f"Welcome, {request.user.username}!"}
    else:
        context = {'welcome_message': None}
    return render(request, 'home.html', context)


def register(request):
    gender_choices = TrukItUser._meta.get_field('gender').choices
    user_type_choices = TrukItUser._meta.get_field('user_type').choices
    context = {
        'gender_choices': gender_choices,
        'user_type_choices': user_type_choices,
    }
    return render(request, 'register.html', context)


def login(request):
    return render(request, 'login.html')


def logout(request):
    return render(request, 'logout.html')


def customer_dashboard(request):
    print('user: ', request.user.is_superuser)
    return render(request, 'customer_dashboard.html')


def driver_dashboard(request):
    print(request.user.truk_it_user)
    return render(request, 'driver_dashboard.html')


def delivery_transactions(request):
    delivery_transactions = DeliveryTransaction.objects.filter(customer=request.user.customer)
    context = {
        'delivery_transactions': delivery_transactions,
    }
    return render(request, 'delivery_transactions.html', context)


def create_delivery_transaction(request):
    if request.method == 'POST':
        inline_form = DeliveryTransactionFormInline(request.POST)
        full_form = DeliveryTransactionForm(request.POST)

        if inline_form.is_valid() and full_form.is_valid():
            cleaned_data_inline = inline_form.cleaned_data
            cleaned_data_full = full_form.cleaned_data

            # Create a new DeliveryItem object with the cleaned data
            new_item = DeliveryItem(**cleaned_data_inline)
            new_item.save()

            # Create a new DeliveryTransaction with the associated DeliveryItem
            transaction = DeliveryTransaction(
                pickup_location_address=cleaned_data_full['pickup_location_address'],
                delivery_location_address=cleaned_data_full['delivery_location_address'],
                request_pickup_timestamp=cleaned_data_full['request_pickup_timestamp'],
                request_delivery_timestamp=cleaned_data_full['request_delivery_timestamp'],
                delivery_item=new_item,
                customer=request.user.customer
            )
            transaction.save()

            return render(redirect('web_delivery_transactions'))
    else:
        inline_form = DeliveryTransactionFormInline(initial={
            'name': '',
            'length': 0,
            'width': 0,
            'height': 0,
            'weight': 0,
            'description': '',
            'pickup_location_address': '',
            'delivery_location_address': '',
            'request_pickup_timestamp': now(),
            'request_delivery_timestamp': now()
        })
        full_form = DeliveryTransactionForm(initial={
            'pickup_location_address': '',
            'delivery_location_address': '',
            'request_pickup_timestamp': now(),
            'request_delivery_timestamp': now()
        })

    return render(request, 'create_delivery_transaction.html', {
        'inline_form': inline_form,
        'full_form': full_form
    })
