from django.urls import path
from apps.store.api.views import search, variation_list, variation_detail, option_list, option_detail, specification_list, specification_detail, product_list, product_detail, category_list, product_review, category_product

# app_name = 'store'

urlpatterns = [
    path('search/', search, name='search'),
    path('category/', category_list, name='category_detail'),
    path('product/', product_list, name='product_list'),
    path('variation/', variation_list, name='variation_list'),
    path('option/', option_list, name='option_list'),
    path('specification/', specification_list, name='specification_list'),

    path('category/<str:slug>/', category_product, name='category_detail'),
    path('product/<str:slug>/', product_detail, name='product_detail'),
    path('variation/<int:product_id>/', variation_detail, name='variation_list'),
    path('option/<int:product>/<int:variation_id>/', option_detail, name='option_detail'),
    path('specification/<int:product>/<int:option_id>/', specification_detail, name='specification_detail'),

    path('product/<str:category_slug>/<str:slug>/review/', product_review, name='product_review'),
    # path('product_variation/', product_variation, name='product_variation'),
]