# from django.core.management.base import BaseCommand
# from apps.store.models import Product, VariationCategory, VariationOption, VariationSpecification

# class Command(BaseCommand):
#     help = 'Populate products and related variations'

#     def handle(self, *args, **kwargs):
#         product_data_list = [
#             # Product data goes here
#         ]
#         variation_data_list = [
#             # Variation data goes here
#         ]

#         for product_data in product_data_list:
#             product = Product.objects.create(**product_data)
#             for variation_data in variation_data_list:
#                 if variation_data['product_name'] == product.name:
#                     variation = VariationCategory.objects.create(product=product, name=variation_data['variation_name'])
#                     for option_data in variation_data['options']:
#                         option = VariationOption.objects.create(variation=variation, name=option_data)
#                         for specification_data in option_data['specifications']:
#                             VariationSpecification.objects.create(option=option, name=specification_data)

# # Use command py manage.py populate_products to run and update