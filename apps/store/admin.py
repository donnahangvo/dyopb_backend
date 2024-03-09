from django.contrib import admin
from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import Category, Product, VariationCategory, VariationOption, VariationSpecification, ProductReview

# Register Store models
admin.site.register(Category)

# Define a form with CKEditor for the Product model
class ProductAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Product
        fields = '__all__'

# Register Product model admin
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm

admin.site.register(VariationCategory)
admin.site.register(VariationOption)
admin.site.register(VariationSpecification)
admin.site.register(ProductReview)



# admin.site.register(Customization)
# admin.site.register(ProductVariation)