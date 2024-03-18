from apps.order.models import Shipping

def create_default_shippings():
    Shipping.objects.create(name='Flat Rate', description='Standard flat rate shipping', rate=10)
    Shipping.objects.create(name='Free Shipping', description='Free shipping for orders over $50', rate=0)

# Run this script to create default shipping options
create_default_shippings()