# import random

# from datetime import datetime

# from django.shortcuts import render, get_object_or_404, redirect
# from django.db.models import Q

# from apps.cart.cart import Cart

# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from django.http import JsonResponse

# from .models import Product, Category, ProductReview

# from .serializers import CategorySerializer, ProductSerializer, VariationSerializer, OptionSerializer, SpecificationSerializer
# from .models import Category, Product, VariationCategory, VariationOption, VariationSpecification

# # create methods for getting information from rest framework to be shown on the frontend

# @api_view(['GET'])
# def search(request):
#     query = request.GET.get('query')
#     instock = request.GET.get('instock')
#     price_from = request.GET.get('price_from', 0)
#     price_to = request.GET.get('price_to', 100000)
#     sorting = request.GET.get('sorting', '-date_added')
#     products = Product.objects.filter(Q(title__icontains=query) | Q(description__icontains=query)).filter(price__gte=price_from).filter(price__lte=price_to)

#     if instock:
#         products = products.filter(num_available__gte=1)

#     serializer = ProductSerializer(products.order_by(sorting), many=True)
#     return Response(serializer.data)


# @api_view(['GET'])
# def variation_list(request):
#     variations = VariationCategory.objects.all()
#     serializer = VariationSerializer(variations, many=True)
#     return Response(serializer.data)

# @api_view(['GET'])
# def option_list(request):
#     options = VariationOption.objects.all()
#     serializer = OptionSerializer(options, many=True)
#     return Response(serializer.data)

# @api_view(['GET'])
# def specification_list(request):
#     specifications = VariationSpecification.objects.all()
#     serializer = SpecificationSerializer(specifications, many=True)
#     return Response(serializer.data)


# @api_view(['GET', 'POST'])
# def product_detail(request, category_slug, slug):
#     if request.method == 'POST' and request.user.is_authenticated:
#         # Add review
#         product = get_object_or_404(Product, slug=slug)
#         stars = request.POST.get('stars', 3)
#         content = request.POST.get('content', '')
#         review = ProductReview.objects.create(product=product, user=request.user, stars=stars, content=content)
#         return redirect('product_detail', category_slug=category_slug, slug=slug)
    
#     # Existing code for GET request
#     product = get_object_or_404(Product, slug=slug)
#     serializer = ProductSerializer(product)
#     return Response(serializer.data)

# @api_view(['GET'])
# def category_detail(request, slug):
#     category = get_object_or_404(Category, slug=slug)
#     serializer = CategorySerializer(category)
#     return Response(serializer.data)
















# Old code not needed
# def search(request):
#     query = request.GET.get('query')
#     instock = request.GET.get('instock')
#     price_from = request.GET.get('price_from', 0)
#     price_to = request.GET.get('price_to', 100000)
#     sorting = request.GET.get('sorting', '-date_added')
#     products = Product.objects.filter(Q(title__icontains=query) | Q(description__icontains=query)).filter(price__gte=price_from).filter(price__lte=price_to)

#     if instock:
#         products = products.filter(num_available__gte=1)

#     context = {
#         'query': query,
#         'products': products.order_by(sorting),
#         'instock': instock,
#         'price_from': price_from,
#         'price_to': price_to,
#         'sorting': sorting
#     }

#     return render(request, 'search.html', context)

# def product_detail(request, category_slug, slug):
#     product = get_object_or_404(Product, slug=slug)
#     product.num_visits = product.num_visits + 1
#     product.last_visit = datetime.now()
#     product.save()

#     # Add review

#     if request.method == 'POST' and request.user.is_authenticated:
#         stars = request.POST.get('stars', 3)
#         content = request.POST.get('content', '')

#         review = ProductReview.objects.create(product=product, user=request.user, stars=stars, content=content)

#         return redirect('product_detail', category_slug=category_slug, slug=slug)

#     #

#     related_products = list(product.category.products.filter(parent=None).exclude(id=product.id))
    
#     if len(related_products) >= 3:
#         related_products = random.sample(related_products, 3)

#     if product.parent:
#         return redirect('product_detail', category_slug=category_slug, slug=product.parent.slug)

#     imagesstring = "{'thumbnail': '%s', 'image': '%s'}," % (product.thumbnail.url, product.image.url)

#     for image in product.images.all():
#         imagesstring = imagesstring + ("{'thumbnail': '%s', 'image': '%s'}," % (image.thumbnail.url, image.image.url))

#     cart = Cart(request)

#     if cart.has_product(product.id):
#         product.in_cart = True
#     else:
#         product.in_cart = False

#     context = {
#         'product': product,
#         'imagesstring': imagesstring,
#         'related_products': related_products
#     }

#     return render(request, 'product_detail.html', context)

# def category_detail(request, slug):
#     category = get_object_or_404(Category, slug=slug)
#     products = category.products.filter(parent=None)

#     context = {
#         'category': category,
#         'products': products
#     }

#     return render(request, 'category_detail.html', context)