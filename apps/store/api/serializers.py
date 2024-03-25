from rest_framework import serializers
from apps.store.models import Image, Category, Product, ProductImage, VariationCategory, VariationOption, VariationSpecification, ProductReview


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('image', 'thumbnail')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'parent', 'name', 'slug', 'category_sku', 'is_featured', 'ordering')

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'category', 'parent', 'name', 'slug', 'product_sku', 'description', 'price', 'is_featured', 'ordering' )

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'product', 'image', 'thumbnail']

class VariationSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariationCategory
        fields = ('id', 'product', 'parent', 'name', 'slug', 'variation_sku', 'description', 'image', 'thumbnail', 'ordering')

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariationOption
        fields = ('id', 'variation', 'parent', 'name', 'slug', 'option_sku', 'description', 'image', 'thumbnail', 'ordering')

class SpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariationSpecification
        fields = ('id', 'option', 'parent', 'name', 'slug', 'specification_sku', 'description', 'num_available', 'is_featured', 'image', 'thumbnail', 'ordering')

class ProductReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductReview
        fields = ('id', 'product', 'user', 'stars', 'content', 'date_added', 'image', 'thumbnail')