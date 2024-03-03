from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from apps.order.models import Order, OrderItem
from apps.cart.cart import Cart

@login_required
def checkout(request):
    # Get user details from the request or use default values
    user = request.user
    if user.is_authenticated:
        first_name = user.first_name
        last_name = user.last_name
        email = user.email
        address = user.userprofile.address
        apartment = user.userprofile.apartment
        city = user.userprofile.city
        state = user.userprofile.state
        zipcode = user.userprofile.zipcode
        country = user.userprofile.country
        phone = user.userprofile.phone
    else:
        # Provide default values if user is not authenticated
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address', '')
        apartment = request.POST.get('apartment', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zipcode = request.POST.get('zipcode', '')
        country = request.POST.get('country', '')
        phone = request.POST.get('phone', '')

    # Create the order
    order = Order.objects.create(
        user=user,
        first_name=first_name,
        last_name=last_name,
        email=email,
        address=address,
        apartment=apartment,
        city=city,
        state=state,
        zipcode=zipcode,
        country=country,
        phone=phone
    )

    # Process cart items
    cart = Cart(request)
    for item in cart:
        OrderItem.objects.create(
            order=order,
            product=item['product'],
            price=item['price'],
            quantity=item['quantity']
        )

    # Clear the cart after checkout
    cart.clear()

    # Return JSON response with order ID
    return JsonResponse({'order_id': order.id})


# import datetime
# import os

# from random import randint

# from apps.cart.cart import Cart

# from apps.order.models import Order, OrderItem

# def checkout(request, first_name, last_name, email, address, apartment, city, state, zipcode, country, phone):
#     order = Order(first_name=first_name, last_name=last_name, email=email, address=address, apartment=apartment, city=city, state=state, zipcode=zipcode, country=country, phone=phone)
    
#     if request.user.is_authenticated:
#         order.user = request.user

#     order.save()

#     cart = Cart(request)

#     for item in cart:
#         OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity'])

#     return order.id