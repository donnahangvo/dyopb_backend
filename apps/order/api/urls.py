from django.urls import path
from apps.order.utils import checkout
from apps.order.api.views import admin_order_pdf


# app_name = 'order'

urlpatterns = [
    path('checkout', checkout, name='checkout'),
    path('admin_order_pdf/<int:order_id>', admin_order_pdf, name='admin_order_pdf'),
]