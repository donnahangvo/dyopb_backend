from django.conf import settings
from django.shortcuts import render, redirect

from .cart import Cart

def cart_detail(request):
    cart = Cart(request)
    productsstring = ''

    for item in cart:
        product = item['product']
        url = '/%s/%s/' % (product.category.slug, product.slug)
        b = "{'id': '%s', 'title': '%s', 'price': '%s', 'quantity': '%s', 'total_price': '%s', 'thumbnail': '%s', 'url': '%s', 'num_available': '%s'}," % (product.id, product.title, product.price, item['quantity'], item['total_price'], product.get_thumbnail, url, product.num_available)

        productsstring = productsstring + b

    if request.user.is_authenticated:
        first_name = request.user.first_name
        last_name = request.user.last_name
        email = request.user.email
        address = request.user.userprofile.address
        apartment = request.user.userprofile.apartment
        city = request.user.userprofile.city
        state = request.user.userprofile.state
        zipcode = request.user.userprofile.zipcode
        country = request.user.userprofile.country
        phone = request.user.userprofile.phone
    else:
        first_name = last_name = email = address = apartment = city = state = zipcode = country = phone = ''

    context = {
        'cart': cart,
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'phone': phone,
        'address': address,
        'apartment': apartment,
        'city': city,
        'state': state,
        'zipcode': zipcode,
        'country': country,
        'pub_key': settings.STRIPE_API_KEY_PUBLISHABLE,
        'pub_key_paypal': settings.PAYPAL_API_KEY_PUBLISHABLE,
        'productsstring': productsstring.rstrip(',')
    }

    return render(request, 'cart.html', context)

def success(request):
    cart = Cart(request)
    cart.clear()
    
    return render(request, 'success.html')