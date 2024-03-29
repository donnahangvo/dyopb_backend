from django.contrib import admin
from django import forms
from ckeditor.widgets import CKEditorWidget
# from mptt.admin import MPTTModelAdmin
from .models import Category, Product, ProductImage, VariationCategory, VariationOption, VariationSpecification, ProductReview
from django.contrib import admin
# from django.core.management import call_command

# Register Store models
admin.site.register(Category)

# Define a form with CKEditor for the Product model
class ProductAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Product
        fields = '__all__'

# Inline admin for ProductImage
class ProductImageInline(admin.TabularInline):
    model = ProductImage

# # add populate_products command to admin
# def populate_products(modeladmin, request, queryset):
#     call_command('populate_products')

# populate_products.short_description = "Generate Product Variations"

# class ProductVariationAdmin(admin.ModelAdmin):
#     actions = [populate_products]


# Register Product model admin
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    inlines = [
        ProductImageInline,
    ]

admin.site.register(VariationCategory)
admin.site.register(VariationOption)
admin.site.register(VariationSpecification)
admin.site.register(ProductReview)


# admin.site.register(ProductVariation, ProductVariationAdmin)
# admin.site.register(Customization)
# admin.site.register(ProductVariation)