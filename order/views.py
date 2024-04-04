import json
import stripe
from config import settings
from django.http import JsonResponse
from django.shortcuts import render,redirect
from .models import Order, OrderItem
from cart.cart import Cart

# Create your views here.
def start_order(request):
    cart = Cart(request)
    data = json.loads(request.body)

    total_price = 0
    items = []
    for item in cart:
        product = item['product']
        total_price += product.price * int(item['quantity'])

        obj = {
            'price_data': {
                'currency': 'kes',
                'product_data': {
                    'name': product.name,
                },
                'unit_amount': product.price,
            },
            'quantity': item['quantity'],
        }
        items.append(obj)


    stripe.api_key = settings.STRIPE_API_KEY_HIDDEN
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=items,
        mode='payment',
        success_url=settings.STRIPE_SUCCESS_URL,
        cancel_url=settings.STRIPE_CANCEL_URL
    )
    payment_intent = session.payment_intent

    first_name = data['first_name']
    last_name = data['last_name']
    email = data['email']
    address = data['address']
    zipcode = data['zipcode']
    place = data['place']
    phone = data['phone']

    order = Order.objects.create( user=request.user, first_name=first_name, last_name=last_name, email=email, address=address, zipcode=zipcode, place=place, phone=phone)

    order.payment_intent = payment_intent
    order.paid_amount = total_price
    order.paid = True
    order.save()

    for item in cart:
        product = item['product']
        quantity = item['quantity']
        price = product.price * quantity

        item = OrderItem.objects.create(order=order, product=product, price= price, quantity=quantity)

    cart.clear()

    return JsonResponse({'session':session, 'order': payment_intent})
