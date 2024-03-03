from django.urls import path
from apps.coupon.api.views import coupon_can_use

urlpatterns = [
    path('coupon', coupon_can_use, name='coupon'),
]