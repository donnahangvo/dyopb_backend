import random

from datetime import datetime

from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q

from apps.cart.cart import Cart

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse

from apps.store.api.serializers import CategorySerializer, ProductSerializer, VariationSerializer, OptionSerializer, SpecificationSerializer
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
def variation_list(request):
    variations = VariationCategory.objects.all()
    serializer = VariationSerializer(variations, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def option_list(request):
    options = VariationOption.objects.all()
    serializer = OptionSerializer(options, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def specification_list(request):
    specifications = VariationSpecification.objects.all()
    serializer = SpecificationSerializer(specifications, many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
def product_detail(request, category_slug, slug):
    if request.method == 'POST' and request.user.is_authenticated:
        # Add review
        product = get_object_or_404(Product, slug=slug)
        stars = request.POST.get('stars', 3)
        content = request.POST.get('content', '')
        review = ProductReview.objects.create(product=product, user=request.user, stars=stars, content=content)
        return redirect('product_detail', category_slug=category_slug, slug=slug)
    
    # Existing code for GET request
    product = get_object_or_404(Product, slug=slug)
    serializer = ProductSerializer(product)
    return Response(serializer.data)

@api_view(['GET'])
def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    serializer = CategorySerializer(category)
    return Response(serializer.data)
