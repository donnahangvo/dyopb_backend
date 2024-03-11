from django.urls import path
from apps.cart.api.views import create_cart, add_to_cart, remove_from_cart
from apps.cart.views import cart_detail, success
from apps.cart.webhook import webhook

urlpatterns = [
    path('cart/detail/', cart_detail, name='cart'),
    path('cart/success/', success, name='success'),
    path('cart/', create_cart, name='create_cart'),
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('webhook/', webhook, name='webhook'),
]