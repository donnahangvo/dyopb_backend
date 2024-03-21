import random

from datetime import datetime

from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q

from apps.cart.cart import Cart

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import JsonResponse

from apps.store.api.serializers import CategorySerializer, ProductSerializer, VariationSerializer, OptionSerializer, SpecificationSerializer, ProductReviewSerializer
from apps.store.models import Category, Product, VariationCategory, VariationOption, VariationSpecification, ProductReview

# create methods for getting information from rest framework to be shown on the frontend

@api_view(['GET'])
def search(request):
    query = request.GET.get('query')
    instock = request.GET.get('instock')
    price_from = request.GET.get('price_from', 0)
    price_to = request.GET.get('price_to', 100000)
    sorting = request.GET.get('sorting', '-date_added')
    products = Product.objects.filter(Q(title__icontains=query) | Q(description__icontains=query)).filter(price__gte=price_from).filter(price__lte=price_to)

    if instock:
        products = products.filter(num_available__gte=1)

    serializer = ProductSerializer(products.order_by(sorting), many=True)
    return Response(serializer.data)


@api_view(['GET'])
def variation_detail(request):
    variations = VariationCategory.objects.all()
    serializer = VariationSerializer(variations, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def option_detail(request):
    options = VariationOption.objects.all()
    serializer = OptionSerializer(options, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def specification_detail(request):
    specifications = VariationSpecification.objects.all()
    serializer = SpecificationSerializer(specifications, many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
def product_detail(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def category_detail(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)

@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def product_review(request, category_slug, slug):
    if request.method == 'GET':
        product = get_object_or_404(Product, slug=slug)
        reviews = product.reviews.all()
        serializer = ProductReviewSerializer(reviews, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        product = get_object_or_404(Product, slug=slug)
        stars = request.data.get('stars', 3)  # Default to 3 stars if not provided
        content = request.data.get('content', '')
        image = request.data.get('image', None)
        thumbnail = request.data.get('thumbnail', None)
        
        review = ProductReview.objects.create(product=product, user=request.user, stars=stars, content=content, image=image, thumbnail=thumbnail)
        serializer = ProductReviewSerializer(review)
        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        review_id = request.data.get('review_id')
        if review_id:
            review = get_object_or_404(ProductReview, id=review_id)
            if review.user == request.user:
                review.delete()
                return Response({"message": "Review deleted successfully"}, status=204)
            else:
                return Response({"error": "You do not have permission to delete this review"}, status=403)
        else:
            return Response({"error": "Review ID is required"}, status=400)