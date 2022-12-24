import mercadopago
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render

from .models import Payment

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


def checkoutpro(request):
    if request.method == 'GET':
        products = Payment.objects.all().filter(pk=1)
        context = {
            'products': products
        }
        return render(request, 'payments/pages/checkoutpro.html', context)

    if request.method == 'POST':
        # Obter o pedido do banco de dados
        order = Payment.objects.get(pk=1)

        # Criar um dicionário com as informações de pagamento
        payment_data = {
            'items': [{
                'title': order.description,
                'quantity': 1,
                'currency_id': order.currency,
                'unit_price':  float(order.value)
            }],
            'payer': {
                'name': 'João da Silva',
                'email': 'joao@example.com'
            }
        }

        # Criar a preferência de pagamento
        preference_response = sdk.preference().create(payment_data)

        # Obter o link para o Checkout Pro
        checkout_url = preference_response['response']['init_point']

        return redirect(checkout_url)


def checkoutproseveralproducts(request):
    if request.method == 'GET':
        products = Payment.objects.all()
        context = {
            'products': products
        }
        return render(request, 'payments/pages/checkoutpro.html', context)

    if request.method == 'POST':
        orders = Payment.objects.all()
        # Criar um dicionário com as informações de pagamento
        payment_data = {
            'items': [],
            'payer': {
                'name': 'João da Silva',
                'email': 'joao@example.com'
            }
        }

        # Adicionar os produtos à lista de items
        for order in orders:
            item = {
                'title': order.description,
                'quantity': 1,
                'currency_id': order.currency,
                'unit_price':  float(order.value)
            }
            print(item)
            payment_data['items'].append(item)

    # Criar a preferência de pagamento
    preference_response = sdk.preference().create(payment_data)

    # Obter o link para o Checkout Pro
    checkout_url = preference_response['response']['init_point']

    return redirect(checkout_url)


def checkoutproselectedproducts(request):
    if request.method == 'GET':
        products = Payment.objects.all()
        context = {
            'products': products
        }
        return render(request, 'payments/pages/checkoutpro.html', context)

    if request.method == 'POST':
        product_ids = [3, 4]
        orders = Payment.objects.filter(pk__in=product_ids)
        # Criar um dicionário com as informações de pagamento
        payment_data = {
            'items': [],
            'payer': {
                'name': 'João da Silva',
                'email': 'joao@example.com'
            }
        }

        # Adicionar os produtos à lista de items
        for order in orders:
            item = {
                'title': order.description,
                'quantity': 1,
                'currency_id': order.currency,
                'unit_price':  float(order.value)
            }
            print(item)
            payment_data['items'].append(item)

    # Criar a preferência de pagamento
    preference_response = sdk.preference().create(payment_data)

    # Obter o link para o Checkout Pro
    checkout_url = preference_response['response']['init_point']

    return redirect(checkout_url)


def checkoutproselectedproductssession(request):
    if request.method == 'GET':
        products = Payment.objects.all()
        # Obter a lista de itens no carrinho da sessão
        cart_items = request.session.get('cart_items')
        context = {
            'products': products,
            'cart_items': cart_items,
        }
        return render(request, 'payments/pages/checkoutpro.html', context)

    if request.method == 'POST':
        product_ids = request.session.get('cart_items')
        for product_id in product_ids:
            quantitly_cart = product_ids[product_id]['quantity']
        orders = Payment.objects.filter(pk__in=product_ids)
        # Criar um dicionário com as informações de pagamento
        payment_data = {
            'items': [],
            'payer': {
                'name': 'João da Silva',
                'email': 'joao@example.com'
            }
        }
        domain = "https://yourdomain.com"
        if settings.DEBUG:
            domain = "http://127.0.0.1:8000"
        payment_data['back_urls'] = {
            "success": domain + "/success/",
            "failure": domain + "/failure/",
            "pending": domain + "/pending/"
        }
        # Adicionar os produtos à lista de items
        for order in orders:
            # Obter a quantidade do item da sessão
            item = {
                'title': order.description,
                'quantity': quantitly_cart,
                'currency_id': order.currency,
                'unit_price':  float(order.value * quantitly_cart)
            }
            payment_data['items'].append(item)

    # Criar a preferência de pagamento
    preference_response = sdk.preference().create(payment_data)

    # Obter o link para o Checkout Pro
    checkout_url = preference_response['response']['init_point']
    return redirect(checkout_url)


def addtocart(request):
    if request.method == 'GET':
        # destruindo a sessão
        # if request.session.get('cart_items'):
        #     del request.session['cart_items']
        #     request.session.save()

        product_id = request.GET.get('product_id')  # Obter o ID do produto
        if not product_id:
            return redirect('checkoutproselectedproductssession')
        product = get_object_or_404(Payment, pk=product_id)

        # Obter a lista de itens no carrinho da sessão
        description = product.description
        value = float(product.value)
        quantity = 1

        if not request.session.get('cart_items'):
            request.session['cart_items'] = {}
            request.session.save()

        cart_items = request.session['cart_items']

        if product_id in cart_items:
            quantitly_cart = cart_items[product_id]['quantity']
            quantitly_cart += 1

            cart_items[product_id]['quantity'] = quantitly_cart
            cart_items[product_id]['value'] = value * quantitly_cart

        else:
            cart_items[product_id] = {
                'product_id': product_id,
                'description': description,
                'value': value,
                'quantity': quantity,
            }
        request.session.save()
        return redirect('checkoutproselectedproductssession')


def removecart(request):
    if request.method == 'GET':
        product_id = request.GET.get('product_id')
        if not product_id:
            return redirect('checkoutproselectedproductssession')

        cart_items = request.session.get('cart_items')
        if product_id in cart_items:
            del cart_items[product_id]
            request.session.save()
        return redirect('checkoutproselectedproductssession')


def success(request):
    request.session.clear()
    return render(request, 'payments/pages/success.html')
