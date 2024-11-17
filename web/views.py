from django.contrib.auth.decorators import login_required
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
    return render(request, 'driver_dashboard.html')


def customer_delivery_transactions(request):
    try:
        customer = request.user.customer
        delivery_transactions = DeliveryTransaction.objects.filter(customer=customer)
    except AttributeError:
        # Handle the case where the user doesn't have a customer
        delivery_transactions = DeliveryTransaction.objects.none()

    context = {
        'delivery_transactions': delivery_transactions,
        'no_customer_message': 'No customer associated with this account.' if delivery_transactions.count() == 0 else None
    }
    return render(request, 'customer_delivery_transactions.html', context)


def driver_delivery_transactions(request):
    try:
        driver = request.user.driver
        delivery_transactions = DeliveryTransaction.objects.filter(driver=driver)
    except AttributeError:
        # Handle the case where the user doesn't have a driver
        delivery_transactions = DeliveryTransaction.objects.none()

    context = {
        'delivery_transactions': delivery_transactions,
        'no_driver_message': 'No driver associated with this account.' if delivery_transactions.count() == 0 else None
    }
    return render(request, 'driver_delivery_transactions.html', context)


@login_required
def create_delivery_transaction(request):
    if request.method == 'POST':
        form = DeliveryTransactionForm(request.POST)
        if form.is_valid():
            delivery = form.save(commit=False)
            delivery.user = request.user
            delivery.save()
            return redirect(f'add_delivery_item/?transaction_id={delivery.id}')
    else:
        form = DeliveryTransactionForm()

    return render(request, 'create_delivery_transaction.html', {'delivery_transaction_form': form})


@login_required
def add_delivery_item(request):
    transaction_id = request.GET.get('transaction_id')
    if not transaction_id:
        return redirect('create_delivery')

    if request.method == 'POST':
        form = DeliveryItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.delivery_transaction = DeliveryTransaction.objects.get(id=transaction_id)
            item.save()

            # Redirect to a new view that shows the choices
            return redirect('choose_action', transaction_id=transaction_id)
    else:
        form = DeliveryItemForm()

    return render(request, 'add_delivery_items.html', {'form': form})


@login_required
def choose_action(request, transaction_id):
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'add_another':
            return redirect(f'add_delivery_item/?transaction_id={transaction_id}')
        elif action == 'submit_and_save':
            # Process the delivery transaction here
            # You might want to call an API endpoint or perform database operations
            # For example:
            # process_delivery(transaction_id)
            return redirect('web_customer_delivery_transactions')  # Or wherever you want to redirect after submission

    # Render the template with the choice options
    return render(request, 'choose_action.html', {
        'transaction_id': transaction_id,
        'can_add_another': True,  # Set this to False if you don't want to allow adding another item
    })


def delivery_transaction_request_successful(request):
    transaction_id = request.GET.get('transaction_id')

    if not transaction_id:
        return redirect('web_customer_dashboard')  # Redirect to home page if no transaction ID

    try:
        transaction = DeliveryTransaction.objects.get(id=transaction_id)

        context = {
            'transaction': transaction,
            'message': 'Delivery requested successfully!',
        }

        return render(request, 'delivery_request_success.html', context)
    except DeliveryTransaction.DoesNotExist:
        return redirect('web_customer_dashboard')
