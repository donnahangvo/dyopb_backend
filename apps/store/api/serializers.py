from rest_framework import serializers
from apps.store.models import ProductImage, Category, Product, VariationCategory, VariationOption, VariationSpecification


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('image', 'thumbnail')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('title', 'category_sku')


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('category', 'title', 'product_sku', 'description', 'price', 'image', 'thumbnail' )

class VariationSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariationCategory
        fields = ('title', 'variation_sku')

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariationOption
        fields = ('title', 'option_sku', 'image', 'thumbnail')

class SpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariationSpecification
        fields = ('title', 'specification_sku', 'image', 'thumbnail')