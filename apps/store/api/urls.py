from django.urls import path
from apps.store.api.views import search, variation_list, option_list, specification_list, product_detail, category_detail, product_review


# app_name = 'store'

urlpatterns = [
    path('search/', search, name='search'),
    path('variation/', variation_list, name='variation_list'),
    path('option/', option_list, name='option_list'),
    path('specification/', specification_list, name='specification_list'),
    path('product/<str:category_slug>/<str:slug>/', product_detail, name='product_detail'),
    path('category/<str:slug>/', category_detail, name='category_detail'),
    path('product/<str:category_slug>/<str:slug>/review/', product_review, name='product_review'),
]