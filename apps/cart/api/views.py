from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
from apps.store.models import Product
from apps.cart.cart import Cart
from django.conf import settings

@csrf_exempt
@require_GET
def create_cart(request):
    cart = Cart(request)
    cart_data = [
        {
            'id': item['id'],
            'product': {
                'id': item['product'].id,
                'name': item['product'].name,
                'price': item['product'].price
            },
            'quantity': item['quantity'],
            'total_price': item['total_price']
        }
        for item in cart
    ]
    return JsonResponse(cart_data, safe=False)

@csrf_exempt
@require_POST
def add_to_cart(request, product_id):
    cart = Cart(request)
    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)
    cart.add(product)
    return JsonResponse({'message': 'Product added to cart successfully'})

@csrf_exempt
def remove_from_cart(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)
    return JsonResponse({'message': 'Product removed from cart successfully'})