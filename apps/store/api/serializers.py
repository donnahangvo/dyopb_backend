from rest_framework import serializers
from apps.store.models import ProductImage, Category, Product, VariationCategory, VariationOption, VariationSpecification, ProductReview


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('image', 'thumbnail')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id','title', 'slug', 'category_sku')

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'title', 'slug', 'product_sku', 'description', 'price', 'image', 'thumbnail' )

class VariationSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariationCategory
        fields = ('id', 'name', 'slug', 'variation_sku')

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariationOption
        fields = ('id', 'name', 'slug', 'option_sku', 'image', 'thumbnail')

class SpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariationSpecification
        fields = ('id', 'name', 'slug', 'specification_sku', 'description', 'image', 'thumbnail')

class ProductReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductReview
        fields = ('id', 'user', 'stars', 'content', 'date_added', 'image', 'thumbnail')