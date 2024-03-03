import json
import stripe

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from apps.cart.cart import Cart
from apps.order.models import Order
from apps.store.utilities import decrement_product_quantity, send_order_confirmation

@csrf_exempt
def webhook(request):
    payload = request.body
    event = None

    stripe.api_key = settings.STRIPE_API_KEY_HIDDEN

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        return JsonResponse({'error': 'Invalid payload'}, status=400)

    if event.type == 'payment_intent.succeeded':
        payment_intent = event.data.object
        
        try:
            order = Order.objects.get(payment_intent=payment_intent.id)
        except Order.DoesNotExist:
            return JsonResponse({'error': 'Order not found'}, status=404)
        
        order.paid = True
        order.save()

        decrement_product_quantity(order)  
        send_order_confirmation(order)
        
        return JsonResponse({'message': 'Payment succeeded'})

    return JsonResponse({'message': 'Unhandled event'}, status=200)



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