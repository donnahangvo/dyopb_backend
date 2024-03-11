from django.urls import path
from apps.store.api.views import search, variation_list, option_list, specification_list, product_detail,category_detail


# app_name = 'store'

urlpatterns = [
    path('search/', search, name='search'),
    path('variations/', variation_list, name='variation_list'),
    path('options/', option_list, name='option_list'),
    path('specifications/', specification_list, name='specification_list'),
    path('products/<str:category_slug>/<str:slug>/', product_detail, name='product_detail'),
    path('categories/<str:slug>/', category_detail, name='category_detail'),
]