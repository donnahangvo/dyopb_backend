import json
import stripe
import logging
import paypalrestsdk

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from apps.order.models import Order
from apps.store.utilities import decrement_product_quantity, send_order_confirmation

logger = logging.getLogger(__name__)

@csrf_exempt
def webhook(request):
    payload = request.body
    event = None

    stripe.api_key = settings.STRIPE_API_KEY_HIDDEN
    paypalrestsdk.api_key = settings.PAYPAL_API_KEY_HIDDEN

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        logger.error(f"Invalid Stripe payload: {e}")
        return JsonResponse({'error': 'Invalid Stripe payload'}, status=400)

    if event.type == 'payment_intent.succeeded':
        payment_intent = event.data.object
        handle_payment_success(payment_intent)

    elif event.type == 'paypal':
        # Assuming the PayPal event object is similar to Stripe's payment_intent object
        payment_intent = event.data.object
        handle_payment_success(payment_intent)

    else:
        logger.info(f"Unhandled event type: {event.type}")
        return JsonResponse({'message': 'Unhandled event'}, status=200)


def handle_payment_success(payment_intent):
    try:
        order = Order.objects.get(payment_intent=payment_intent.id)
    except Order.DoesNotExist:
        logger.error(f"Order not found for payment intent: {payment_intent.id}")
        return JsonResponse({'error': 'Order not found'}, status=404)

    order.paid = True
    order.save()

    try:
        decrement_product_quantity(order)
        send_order_confirmation(order)
    except Exception as e:
        logger.error(f"Error processing order: {e}")
        # Handle the error appropriately, e.g., notify admins

    return JsonResponse({'message': 'Payment succeeded'})




# import json
# import stripe

# from django.conf import settings
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt

# from apps.cart.cart import Cart
# from apps.order.models import Order
# from apps.store.utilities import decrement_product_quantity, send_order_confirmation

# @csrf_exempt
# def webhook(request):
#     payload = request.body
#     event = None

#     stripe.api_key = settings.STRIPE_API_KEY_HIDDEN
#     paypal.api_key = settings.PAYPAL_API_KEY_HIDDEN
#     stripe_event_types = ['payment_intent.succeeded']

    
#     try:
#         event = stripe.Event.construct_from(
#             json.loads(payload), stripe.api_key
#         )
#     except ValueError as e:
#         logger.error(f"Invalid payload: {e}")
#         return JsonResponse({'error': 'Invalid payload'}, status=400)

#     if event.type in stripe_event_types:
#     # if event.type == 'payment_intent.succeeded':
#         payment_intent = event.data.object
        
#         try:
#             order = Order.objects.get(payment_intent=payment_intent.id)
#         except Order.DoesNotExist:
#             return JsonResponse({'error': 'Order not found'}, status=404)
        
#         order.paid = True
#         order.save()

#         decrement_product_quantity(order)  
#         send_order_confirmation(order)

#         return JsonResponse({'message': 'Payment succeeded'})
    
#     elif event.type == 'paypal':
#                 payment_intent = event.data.object
        
#         try:
#             order = Order.objects.get(payment_intent=payment_intent.id)
#         except Order.DoesNotExist:
#             return JsonResponse({'error': 'Order not found'}, status=404)
        
#         order.paid = True
#         order.save()

#         decrement_product_quantity(order)  
#         send_order_confirmation(order)
        
#         return JsonResponse({'message': 'Payment succeeded'})

# return JsonResponse({'message': 'Unhandled event'}, status=200)



# import json
# import stripe

# from django.conf import settings
# from django.http import HttpResponse
# from django.views.decorators.csrf import csrf_exempt

# from .cart import Cart

# from apps.order.models import Order
# from apps.store.utilities import decrement_product_quantity, send_order_confirmation

# @csrf_exempt
# def webhook(request):
#     payload = request.body
#     event = None

#     stripe.api_key = settings.STRIPE_API_KEY_HIDDEN

#     try:
#         event = stripe.Event.construct_from(
#             json.loads(payload), stripe.api_key
#         )
#     except ValueError as e:
#         return HttpResponse(status=400)

#     if event.type == 'payment_intent.succeeded':
#         payment_intent = event.data.object
        
#         order = Order.objects.get(payment_intent=payment_intent.id)
#         order.paid = True
#         order.save()

#         decrement_product_quantity(order)  
#         send_order_confirmation(order)
        
#     return HttpResponse(status=200)