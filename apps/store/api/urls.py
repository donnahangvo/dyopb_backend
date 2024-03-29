from django.urls import path
from apps.store.api.views import search, variation_detail, option_detail, specification_detail, product_detail, category_detail, product_review


# app_name = 'store'

urlpatterns = [
    path('search/', search, name='search'),
    path('variation/', variation_detail, name='variation_list'),
    path('option/', option_detail, name='option_list'),
    path('specification/', specification_detail, name='specification_list'),
    path('product/', product_detail, name='product_detail'),
    path('category/', category_detail, name='category_detail'),
    # path('product_variation/', product_variation, name='product_variation'),
    path('product/<str:category_slug>/<str:slug>/review/', product_review, name='product_review'),
]