from django.http import JsonResponse
from apps.coupon.models import Coupon
from .serializers import CouponSerializer 

def coupon_can_use(request):
    coupon_code = request.GET.get('coupon_code', '')
    json_response = {}

    try:
        coupon = Coupon.objects.get(code=coupon_code)

        # Use the CouponSerializer to serialize the coupon object
        serializer = CouponSerializer(coupon)

        if coupon.can_use():
            json_response = {'amount': serializer.data['value']}  # Use the serialized value
        else:
            json_response = {'amount': 0}
    except Coupon.DoesNotExist:
        json_response = {'amount': 0}

    return JsonResponse(json_response)



# from django.http import JsonResponse

# from .models import Coupon

# def api_can_use(request):
#     json_response = {}

#     coupon_code = request.GET.get('coupon_code', '')

#     try:
#         coupon = Coupon.objects.get(code=coupon_code)

#         if coupon.can_use():
#             json_response = {'amount': coupon.value}
#         else:
#             json_response = {'amount': 0}
#     except Exception:
#         json_response = {'amount': 0}

#     return JsonResponse(json_response)