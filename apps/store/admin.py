from django.contrib import admin
from django import forms
from ckeditor.widgets import CKEditorWidget
from mptt.admin import MPTTModelAdmin
from .models import Category, Product, ProductImage, VariationCategory, VariationOption, VariationSpecification, ProductReview

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

# Inline admin for VariationCategory
class VariationCategoryInline(admin.TabularInline):
    model = VariationCategory

# # Inline admin for VariationOption
# class VariationOptionInline(admin.TabularInline):
#     model = VariationOption

# # Inline admin for VariationSpecification
# class VariationSpecificationInline(admin.TabularInline):
#     model = VariationSpecification

# Register Product model admin
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    inlines = [
        ProductImageInline,
        VariationCategoryInline,
    ]

admin.site.register(VariationCategory, MPTTModelAdmin)
admin.site.register(VariationOption)
admin.site.register(VariationSpecification)
admin.site.register(ProductReview)



# admin.site.register(Customization)
# admin.site.register(ProductVariation)