from rest_framework import serializers
from apps.coupon.models import Coupon

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ['id', 'code', 'value', 'active', 'num_available', 'num_used']