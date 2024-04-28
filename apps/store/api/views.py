import random

from datetime import datetime

from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q

from apps.cart.cart import Cart

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import JsonResponse

from apps.store.api.serializers import CategorySerializer, ProductSerializer, ProductImageSerializer, VariationSerializer, OptionSerializer, SpecificationSerializer, ProductReviewSerializer
from apps.store.models import Category, Product, ProductImage, VariationCategory, VariationOption, VariationSpecification, ProductReview

# create methods for getting information from rest framework to be shown on the frontend

@api_view(['GET'])
def category_list(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def product_list(request):
    # Retrieve all products
    products = Product.objects.all()
    
    # Serialize each product along with its images
    serialized_products = []
    for product in products:
        serialized_product = ProductSerializer(product).data
        serialized_product['images'] = ProductImageSerializer(product.images.all(), many=True).data
        serialized_products.append(serialized_product)
    
    # Return serialized products as a response
    return Response(serialized_products)

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



@api_view(['GET'])
def category_product(request, slug):
    # Retrieve the category based on the slug
    category = get_object_or_404(Category, slug=slug)
    
    # Retrieve products associated with the category
    products = Product.objects.filter(category=category)
    
    # Serialize the products
    serialized_products = ProductSerializer(products, many=True).data

        # Serialize the products along with their images
    serialized_products = []
    for product in products:
        serialized_product = ProductSerializer(product).data
        serialized_product['images'] = ProductImageSerializer(product.images.all(), many=True).data
        serialized_products.append(serialized_product)
    
    return Response(serialized_products)


# @api_view(['GET'])
# def product_detail(request, slug):
#     # Retrieve the product based on the category_slug and slug
#     product = get_object_or_404(Product, slug=slug)

#         # Serialize the product along with its images
#     serialized_product = ProductSerializer(product).data
#     serialized_product['images'] = ProductImageSerializer(product.images.all(), many=True).data
    
#     return Response(serialized_product)   


# @api_view(['GET'])
# def product_detail(request, slug):
#     # Retrieve the product based on the category_slug and slug
#     product = get_object_or_404(Product, slug=slug)

#     # Serialize the product along with its images
#     serialized_product = ProductSerializer(product).data
#     serialized_product['images'] = ProductImageSerializer(product.images.all(), many=True).data
    
#     # Optionally, include variations in the serialized product
#     serialized_product['variations'] = []
#     for variation in product.variation.all():
#         serialized_variation = {
#             'id': variation.id,
#             'name': variation.name,
#             # Add other variation fields as needed
#         }
#         serialized_product['variations'].append(serialized_variation)

#     return Response(serialized_product)

@api_view(['GET'])
def product_detail(request, slug):
    # Retrieve the product based on the category_slug and slug
    product = get_object_or_404(Product, slug=slug)

    # Serialize the product along with its images
    serialized_product = ProductSerializer(product).data
    serialized_product['images'] = ProductImageSerializer(product.images.all(), many=True).data
    
    # Optionally, include variations in the serialized product
    serialized_product['variations'] = []

    for variation in product.variation.all():
        serialized_variation = {
            'id': variation.id,
            'name': variation.name,
            # Add other variation fields as needed
        }
        # Include options associated with this variation
        serialized_variation['options'] = []

        for option in variation.option.all():
            serialized_option = {
                'id': option.id,
                'name': option.name,
                # Add other option fields as needed
            }
            # Include specifications associated with this option
            serialized_option['specifications'] = []

            for specification in option.specification.all():
                serialized_specification = {
                    'id': specification.id,
                    'name': specification.name,
                    # Add other specification fields as needed
                }
                serialized_option['specifications'].append(serialized_specification)

            serialized_variation['options'].append(serialized_option)

        serialized_product['variations'].append(serialized_variation)

    return Response(serialized_product)



@api_view(['GET'])
def variation_detail(request, product_id):
    # Get the product instance associated with the provided product_id
    product = get_object_or_404(Product, id=product_id)
    
    # Get all variations associated with the product
    variations = VariationCategory.objects.filter(product=product)
    
    # Serialize variations
    serialized_variations = VariationSerializer(variations, many=True).data

    return Response(serialized_variations)


@api_view(['GET'])
def option_detail(request, product, variation_id):
    # Get the variation instance associated with the provided product_id and variation_id
    variation = get_object_or_404(VariationCategory, product=product, id=variation_id)

    # Get all options associated with the variation
    options = VariationOption.objects.filter(variation=variation)

    # Serialize options
    serialized_options = OptionSerializer(options, many=True).data
    return Response(serialized_options)


@api_view(['GET'])
def specification_detail(request, product, option_id):
    # Get the option instance associated with the provided product_id and option_id
    option = get_object_or_404(VariationOption, variation__product=product, id=option_id)

    # Get all specifications associated with the option
    specifications = VariationSpecification.objects.filter(option=option)

    # Serialize specifications
    serialized_specifications = SpecificationSerializer(specifications, many=True).data
    return Response(serialized_specifications)

@api_view(['GET'])
def specification_detail_individual(request, product, option_id, specification_id):
    # Get the option instance associated with the provided product ID and option ID
    option = get_object_or_404(VariationOption, variation__product=product, id=option_id)

    # Get the individual specification associated with the option and specification ID
    specification = get_object_or_404(VariationSpecification, option=option, id=specification_id)

    # Serialize specification
    serialized_specification = SpecificationSerializer(specification).data
    
    return Response(serialized_specification)

# @api_view(['GET'])
# def specification_detail_image(request, specification_id):

#     # Get the individual specification associated with the option and specification ID
#     specification = get_object_or_404(VariationSpecification, id=specification_id)

#     # Serialize specification
#     serialized_specification = SpecificationSerializer(specification).data
    
#     return Response(serialized_specification)






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
        




        # @api_view(['GET'])
# def product_variation(request, product_id):
#     product = Product.objects.get(pk=product_id)
#     variations = product.productvariation_set.all()
#     options = VariationOption.objects.filter(variation__in=variations)
#     specifications = VariationSpecification.objects.filter(option__in=options)
    
#     product_data = ProductSerializer(product).data
#     variation_data = VariationSerializer(variations, many=True).data
#     option_data = OptionSerializer(options, many=True).data
#     specification_data = SpecificationSerializer(specifications, many=True).data
    
#     response_data = {
#         'product': product_data,
#         'variations': variation_data,
#         'options': option_data,
#         'specifications': specification_data,
#     }
#     return Response(response_data)
