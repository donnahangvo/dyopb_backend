from django.urls import path
from apps.order.utils import checkout
from apps.order.api.views import calculate_shipping


# app_name = 'order'

urlpatterns = [
    path('checkout/', checkout, name='checkout'),
    path('shipping/', calculate_shipping, name='shipping'),
]