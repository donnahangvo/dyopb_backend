# # moved to apps.cart.api.views.py
# import json
# import stripe

# from django.conf import settings
# from django.core.exceptions import ObjectDoesNotExist
# from django.http import JsonResponse
# from django.shortcuts import get_object_or_404

# from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment
# from paypalcheckoutsdk.orders import OrdersCaptureRequest

# from apps.cart.cart import Cart
# from apps.order.models import Order
# from apps.coupon.models import Coupon
# from apps.order.utils import checkout, decrement_product_quantity, send_order_confirmation
# from .models import Product


# def create_checkout_session(request):
#     data = json.loads(request.body)

#     # Coupon
#     coupon_code = data.get('coupon_code', '')
#     coupon_value = 0

#     if coupon_code:
#         try:
#             coupon = Coupon.objects.get(code=coupon_code)

#             if coupon.can_use():
#                 coupon_value = coupon.value
#                 coupon.use()
#         except ObjectDoesNotExist:
#             pass

#     # Cart items
#     cart = Cart(request)
#     items = []

#     for item in cart:
#         product = item['product']
#         price = int(product.price * 100)

#         if coupon_value > 0:
#             price = int(price * (int(coupon_value) / 100))

#         obj = {
#             'price_data': {
#                 'currency': 'usd',
#                 'product_data': {
#                     'name': product.title
#                 },
#                 'unit_amount': price
#             },
#             'quantity': item['quantity']
#         }

#         items.append(obj)

#     # Payment gateway
#     gateway = data.get('gateway', '')
#     session = ''
#     order_id = ''
#     payment_intent = ''
    
#     if gateway == 'stripe':
#         stripe.api_key = settings.STRIPE_API_KEY_HIDDEN
#         session = stripe.checkout.Session.create(
#             payment_method_types=['card'],
#             line_items=items,
#             mode='payment',
#             success_url='https://dyopb-backend.onrender.com/cart/success/',
#             cancel_url='https://dyopb-backend.onrender.com/cart/'
#         )
#         payment_intent = session.payment_intent

#     # Create order
#     order_id = checkout(request, data.get('first_name'), data.get('last_name'), data.get('email'),
#                         data.get('address'), data.get('zipcode'), data.get('place'), data.get('phone'))

#     total_price = sum(float(item['product'].price) * int(item['quantity']) for item in cart)
#     if coupon_value > 0:
#         total_price *= (coupon_value / 100)

#     # PayPal
#     if gateway == 'paypal':
#         order_id = data.get('order_id')
#         environment = SandboxEnvironment(client_id=settings.PAYPAL_API_KEY_PUBLISHABLE, 
#                                          client_secret=settings.PAYPAL_API_KEY_HIDDEN)
#         client = PayPalHttpClient(environment)
#         request = OrdersCaptureRequest(order_id)
#         response = client.execute(request)

#         order = Order.objects.get(pk=order_id)
#         order.paid_amount = total_price
#         order.used_coupon = coupon_code

#         if response.result.status == 'COMPLETED':
#             order.paid = True
#             order.payment_intent = order_id
#             order.save()

#             decrement_product_quantity(order)
#             send_order_confirmation(order)
#         else:
#             order.paid = False
#             order.save()
#     else:
#         order = Order.objects.get(pk=order_id)
#         if gateway == 'stripe':
#             order.payment_intent = payment_intent['id']
#         else:
#             order.payment_intent = payment_intent
#         order.paid_amount = total_price
#         order.used_coupon = coupon_code
#         order.save()

#     return JsonResponse({'session': session, 'order': payment_intent})


# def checkout_add_to_cart(request):
#     data = json.loads(request.body)
#     product_id = data.get('product_id')
#     quantity = data.get('quantity', 1)
#     update = data.get('update', False)

#     json_response = {'success': True}

#     cart = Cart(request)
#     product = get_object_or_404(Product, pk=product_id)

#     if not update:
#         cart.add(product=product, quantity=1, update_quantity=False)
#     else:
#         cart.add(product=product, quantity=quantity, update_quantity=True)
    
#     return JsonResponse(json_response)


# def checkout_remove_from_cart(request):
#     data = json.loads(request.body)
#     product_id = data.get('product_id')

#     json_response = {'success': True}

#     cart = Cart(request)
#     cart.remove(product_id)

#     return JsonResponse(json_response)


# # maybe not part of main app?
# import json
# import stripe

# from django.conf import settings
# from django.core.mail import EmailMultiAlternatives
# from django.http import JsonResponse, HttpResponse
# from django.shortcuts import get_object_or_404, redirect
# from django.template.loader import render_to_string

# from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment
# from paypalcheckoutsdk.orders import OrdersCaptureRequest

# from apps.cart.cart import Cart
# from apps.order.views import render_to_pdf

# from apps.order.utils import checkout

# from .models import Product
# from apps.order.models import Order
# from apps.coupon.models import Coupon

# from .utilities import decrement_product_quantity, send_order_confirmation

# def create_checkout_session(request):
#     data = json.loads(request.body)

#     # Coupon 

#     coupon_code = data['coupon_code']
#     coupon_value = 0

#     if coupon_code != '':
#         coupon = Coupon.objects.get(code=coupon_code)

#         if coupon.can_use():
#             coupon_value = coupon.value
#             coupon.use()

#     #

#     cart = Cart(request)
#     items = []
    
#     for item in cart:
#         product = item['product']

#         price = int(product.price * 100)

#         if coupon_value > 0:
#             price = int(price * (int(coupon_value) / 100))

#         obj = {
#             'price_data': {
#                 'currency': 'usd',
#                 'product_data': {
#                     'name': product.title
#                 },
#                 'unit_amount': price
#             },
#             'quantity': item['quantity']
#         }

#         items.append(obj)

#     gateway = data['gateway']
#     session = ''
#     order_id = ''
#     payment_intent = ''
    
#     if gateway == 'stripe':
#         stripe.api_key = settings.STRIPE_API_KEY_HIDDEN
#         session = stripe.checkout.Session.create(
#             payment_method_types=['card'],
#             line_items=items,
#             mode='payment',
#             success_url='https://dyopb-backend.onrender.com/cart/success/',
#             cancel_url='https://dyopb-backend.onrender.com/cart/'
#         )
#         payment_intent = session.payment_intent

#     #
#     # Create order

#     orderid = checkout(request, data['first_name'], data['last_name'], data['email'], data['address'], data['zipcode'], data['place'], data['phone'])

#     total_price = 0.00

#     for item in cart:
#         product = item['product']
#         total_price = total_price + (float(product.price) * int(item['quantity']))

#     if coupon_value > 0:
#         total_price = total_price * (coupon_value / 100)
    

    
#     # PayPal

#     if gateway == 'paypal':
#         order_id = data['order_id']
#         environment = SandboxEnvironment(client_id=settings.PAYPAL_API_KEY_PUBLISHABLE, client_secret=settings.PAYPAL_API_KEY_HIDDEN)
#         client = PayPalHttpClient(environment)

#         request = OrdersCaptureRequest(order_id)
#         response = client.execute(request)

#         order = Order.objects.get(pk=orderid)
#         order.paid_amount = total_price
#         order.used_coupon = coupon_code

#         if response.result.status == 'COMPLETED':
#             order.paid = True
#             order.payment_intent = order_id
#             order.save()

#             decrement_product_quantity(order)
#             send_order_confirmation(order)
#         else:
#             order.paid = False
#             order.save()
#     else:
#         order = Order.objects.get(pk=orderid)
#         if gateway == 'stripe':
#             order.payment_intent = payment_intent['id']
#         else:
#             order.payment_intent = payment_intent
#         order.paid_amount = total_price
#         order.used_coupon = coupon_code
#         order.save()

#     #

#     return JsonResponse({'session': session, 'order': payment_intent})

# def checkout_add_to_cart(request):
#     data = json.loads(request.body)
#     jsonresponse = {'success': True}
#     product_id = data['product_id']
#     update = data['update']
#     quantity = data['quantity']

#     cart = Cart(request)

#     product = get_object_or_404(Product, pk=product_id)

#     if not update:
#         cart.add(product=product, quantity=1, update_quantity=False)
#     else:
#         cart.add(product=product, quantity=quantity, update_quantity=True)
    
#     return JsonResponse(jsonresponse)

# def checkout_remove_from_cart(request):
#     data = json.loads(request.body)
#     jsonresponse = {'success': True}
#     product_id = str(data['product_id'])

#     cart = Cart(request)
#     cart.remove(product_id)

#     return JsonResponse(jsonresponse)