from django.contrib import admin

from .models import Category, Product, VariationCategory, VariationOption, VariationSpecification, ProductReview

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(VariationCategory)
admin.site.register(VariationOption)
admin.site.register(VariationSpecification)
# admin.site.register(Customization)
# admin.site.register(ProductVariation)
admin.site.register(ProductReview)