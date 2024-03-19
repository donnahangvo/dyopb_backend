from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .cart import Cart
import stripe

@csrf_exempt
def cart_detail(request):
    if request.method == 'GET':
        cart = Cart(request)
        products = []

        # Get user data
        user_data = {}
        if request.user.is_authenticated:
            user_profile = request.user.userprofile
            user_data = {
                'address1': user_profile.address1,
                'address2': user_profile.address2,
                'city': user_profile.city,
                'state': user_profile.state,
                'zipcode': user_profile.zipcode,
                'country': user_profile.country
            }

        # Calculate taxes
        shipping_address = {
            'line1': user_data.get('address1', ''),
            'line2': user_data.get('address2', ''),
            'city': user_data.get('city', ''),
            'state': user_data.get('state', ''),
            'postal_code': user_data.get('zipcode', ''),
            'country': user_data.get('country', '')
        }

        line_items = []
        for item in cart:
            product = item['product']
            line_item = {
                'price_data': {
                    'currency': 'usd',
                    'unit_amount': int(product.price * 100),
                    'product_data': {
                        'name': product.title,
                        'description': product.description,
                    },
                },
                'quantity': item['quantity'],
            }
            line_items.append(line_item)

        try:
            # Call Stripe Tax to calculate taxes
            stripe.api_key = settings.STRIPE_SECRET_KEY
            tax_rates = stripe.TaxRate.list()
            tax_rates_dict = {rate.id: rate for rate in tax_rates}
            tax_calculation = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                shipping_address=shipping_address,
                tax_rates=[tax_rates_dict['TAX_RATE_ID']],  # Replace TAX_RATE_ID with actual tax rate ID
            )
            total_tax_amount = sum([item.amount for item in tax_calculation.total_details.line_item_details])
        except stripe.error.StripeError as e:
            return JsonResponse({'error': str(e)}, status=500)

        for item in cart:
            product = item['product']
            url = '/%s/%s/' % (product.category.slug, product.slug)
            product_data = {
                'id': product.id,
                'title': product.title,
                'price': product.price,
                'quantity': item['quantity'],
                'total_price': item['total_price'],
                'thumbnail': product.get_thumbnail,
                'url': url,
                'num_available': product.num_available
            }
            products.append(product_data)

        context = {
            'cart': products,
            'total_tax_amount': total_tax_amount / 100,  # Convert back to dollars
            'pub_key': settings.STRIPE_API_KEY_PUBLISHABLE,
            'pub_key_paypal': settings.PAYPAL_API_KEY_PUBLISHABLE,
            **user_data
        }

        return JsonResponse(context)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


def success(request):
    cart = Cart(request)
    cart.clear()
    
    return JsonResponse({'message': 'Success! Cart cleared.'})

# from django.conf import settings
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt 
# from .cart import Cart
# import stripe

# @csrf_exempt
# def cart_detail(request):
#     if request.method == 'GET':
#         cart = Cart(request)
#         products = []

#         # Calculate taxes
#         # Retrieve customer shipping address
#         shipping_address = {
#             'line1': user_data.get('address1', ''),
#             'line2': user_data.get('address2', ''),
#             'city': user_data.get('city', ''),
#             'state': user_data.get('state', ''),
#             'postal_code': user_data.get('zipcode', ''),
#             'country': user_data.get('country', '')
#         }

#         # Prepare line items for tax calculation
#         line_items = []
#         for item in cart:
#             product = item['product']
#             line_item = {
#                 'price_data': {
#                     'currency': 'usd',  # Adjust currency as needed
#                     'unit_amount': int(product.price * 100),  # Convert to cents
#                     'product_data': {
#                         'name': product.title,
#                         'description': product.description,
#                     },
#                 },
#                 'quantity': item['quantity'],
#             }
#             line_items.append(line_item)

#         # Call Stripe Tax to calculate taxes
#         try:
#             tax_rates = stripe.TaxRate.list()
#             tax_rates_dict = {rate.id: rate for rate in tax_rates}
#             tax_calculation = stripe.checkout.Session.create(
#                 payment_method_types=['card'],
#                 line_items=line_items,
#                 shipping_address=shipping_address,
#                 tax_rates=[tax_rates_dict['TAX_RATE_ID']],  # Replace TAX_RATE_ID with actual tax rate ID this will be provided once website goes live
#             )
#             total_tax_amount = sum([item.amount for item in tax_calculation.total_details.line_item_details])
#         except stripe.error.StripeError as e:
#             return JsonResponse({'error': str(e)}, status=500)

#         for item in cart:
#             product = item['product']
#             url = '/%s/%s/' % (product.category.slug, product.slug)
#             product_data = {
#                 'id': product.id,
#                 'title': product.title,
#                 'price': product.price,
#                 'quantity': item['quantity'],
#                 'total_price': item['total_price'],
#                 'thumbnail': product.get_thumbnail,
#                 'url': url,
#                 'num_available': product.num_available
#             }
#             products.append(product_data)

#         user_data = {}
#         if request.user.is_authenticated:
#             user_profile = request.user.userprofile
#             user_data = {
#                 'first_name': request.user.first_name,
#                 'last_name': request.user.last_name,
#                 'email': request.user.email,
#                 'address1': user_profile.address1,
#                 'address2': user_profile.address2,
#                 'city': user_profile.city,
#                 'state': user_profile.state,
#                 'zipcode': user_profile.zipcode,
#                 'country': user_profile.country,
#                 'phone': user_profile.phone
#             }

#         context = {
#             'cart': products,
#             **user_data,
#             'total_tax_amount': total_tax_amount / 100,  # Convert back to dollars
#             'pub_key': settings.STRIPE_API_KEY_PUBLISHABLE,
#             'pub_key_paypal': settings.PAYPAL_API_KEY_PUBLISHABLE,
#         }

#         return JsonResponse(context)
#     else:
#         return JsonResponse({'error': 'Method not allowed'}, status=405)


# from django.conf import settings
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt 
# from .cart import Cart

# @csrf_exempt  # Add this decorator to allow POST requests from external domains
# def cart_detail(request):
#     if request.method == 'GET':  # Allow only GET requests
#         cart = Cart(request)
#         products = []

#         for item in cart:
#             product = item['product']
#             url = '/%s/%s/' % (product.category.slug, product.slug)
#             product_data = {
#                 'id': product.id,
#                 'title': product.title,
#                 'price': product.price,
#                 'quantity': item['quantity'],
#                 'total_price': item['total_price'],
#                 'thumbnail': product.get_thumbnail,
#                 'url': url,
#                 'num_available': product.num_available
#             }
#             products.append(product_data)

#         user_data = {}
#         if request.user.is_authenticated:
#             user_profile = request.user.userprofile
#             user_data = {
#                 'first_name': request.user.first_name,
#                 'last_name': request.user.last_name,
#                 'email': request.user.email,
#                 'address1': user_profile.address1,
#                 'address2': user_profile.address2,
#                 'city': user_profile.city,
#                 'state': user_profile.state,
#                 'zipcode': user_profile.zipcode,
#                 'country': user_profile.country,
#                 'phone': user_profile.phone
#             }

#         context = {
#             'cart': products,
#             **user_data,
#             'pub_key': settings.STRIPE_API_KEY_PUBLISHABLE,
#             'pub_key_paypal': settings.PAYPAL_API_KEY_PUBLISHABLE,
#         }

#         return JsonResponse(context)
#     else:
#         return JsonResponse({'error': 'Method not allowed'}, status=405)  # Return error for non-GET requests

# def success(request):
#     cart = Cart(request)
#     cart.clear()
    
#     return JsonResponse({'message': 'Success! Cart cleared.'})






# from django.conf import settings
# from django.shortcuts import render, redirect

# from .cart import Cart

# def cart_detail(request):
#     cart = Cart(request)
#     productsstring = ''

#     for item in cart:
#         product = item['product']
#         url = '/%s/%s/' % (product.category.slug, product.slug)
#         b = "{'id': '%s', 'title': '%s', 'price': '%s', 'quantity': '%s', 'total_price': '%s', 'thumbnail': '%s', 'url': '%s', 'num_available': '%s'}," % (product.id, product.title, product.price, item['quantity'], item['total_price'], product.get_thumbnail, url, product.num_available)

#         productsstring = productsstring + b

#     if request.user.is_authenticated:
#         first_name = request.user.first_name
#         last_name = request.user.last_name
#         email = request.user.email
#         address = request.user.userprofile.address
#         apartment = request.user.userprofile.apartment
#         city = request.user.userprofile.city
#         state = request.user.userprofile.state
#         zipcode = request.user.userprofile.zipcode
#         country = request.user.userprofile.country
#         phone = request.user.userprofile.phone
#     else:
#         first_name = last_name = email = address = apartment = city = state = zipcode = country = phone = ''

#     context = {
#         'cart': cart,
#         'first_name': first_name,
#         'last_name': last_name,
#         'email': email,
#         'phone': phone,
#         'address': address,
#         'apartment': apartment,
#         'city': city,
#         'state': state,
#         'zipcode': zipcode,
#         'country': country,
#         'pub_key': settings.STRIPE_API_KEY_PUBLISHABLE,
#         'pub_key_paypal': settings.PAYPAL_API_KEY_PUBLISHABLE,
#         'productsstring': productsstring.rstrip(',')
#     }

#     return render(request, 'cart.html', context)

# def success(request):
#     cart = Cart(request)
#     cart.clear()
    
#     return render(request, 'success.html')