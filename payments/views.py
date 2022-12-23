import mercadopago
from django.conf import settings
from django.shortcuts import render

# Create your views here.
sdk = mercadopago.SDK(settings.ACCESS_TOKEN)


def home(request):
    new_customer = {
        "email": "test1@gmail.com",
        "first_name": "Test",
        "last_name": "User",
    }
    result = sdk.customer().create(new_customer)

    if result['status'] == 201:
        customer_id = result['response']['id']
        print("Customer created with ID:", customer_id)
        return render(request, 'payments/pages/home.html')
    else:
        print("Error creating customer:", result['response']['message'])
        return render(request, 'payments/pages/home.html')


def filter(request):
    filters = {
        "email": "asc"
    }

    customers_response = sdk.customer().search(filters=filters)
    customers = customers_response["response"]
    print(customers)
    return render(request, 'payments/pages/home.html')


def update(request):
    customer_id = '1201321128-y3wTdj4gccNkBP'
    customer_data = {
        "first_name": 'heitor',
        "last_name": 'wagner',
    }

    customer_response = sdk.customer().update(customer_id, customer_data)
    customer = customer_response["response"]
    print(customer)
    return render(request, 'payments/pages/home.html')


def payment(request):
    payment_data = {
        "transaction_amount": 100,
        "token": 'ff8080814c11e237014c1ff593b57b4d',
        "installments": 1,
        "payer": {
            "type": "customer",
            "id": "1271610551-ptywVIJWkv7G8l"
        }
    }

    payment_response = sdk.payment().create(payment_data)
    payment = payment_response["response"]
    print(payment)
    return render(request, 'payments/pages/home.html')


def checkoutpro(request):
    # Cria um item na preferência
    return render(request, 'payments/pages/checkoutpro.html')
