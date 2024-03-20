"""
URL configuration for dyopb_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.contrib.auth import views

from apps.order.views import admin_order_pdf
from .sitemaps import StaticViewSitemap, CategorySitemap, ProductSitemap

sitemaps = {'static': StaticViewSitemap, 'product': ProductSitemap, 'category': CategorySitemap}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/admin_order_pdf/<int:order_id>/', admin_order_pdf, name='admin_order_pdf'),

    # Auth
    path('api/', include('apps.userprofile.api.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    # Cart, Coupon, Newsletter, Orders

    path('api/', include('apps.coupon.api.urls')),
    path('api/', include('apps.newsletter.api.urls')),
    path('api/', include('apps.order.api.urls')),
    path('api/', include('apps.cart.api.urls')),

    # Store
    path('api/', include('apps.store.api.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)







# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('admin/admin_order_pdf/<int:order_id>/', include('apps.order.api.urls')),

#     # Auth
#     path('api/', include('apps.userprofile.api.urls')),

#     # path('api/signup/', include('apps.userprofile.api.urls')),
#     # path('api/login/', include('apps.userprofile.api.urls')),
#     # path('api/logout/', include('apps.userprofile.api.urls')),
#     # path('api/myaccount/', include('apps.userprofile.api.urls')),
    
#     path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

#     # Cart, Coupon, Newsletter, Orders

#     path('api/', include('apps.coupon.api.urls')),
#     path('api/', include('apps.newsletter.api.urls')),
#     path('api/', include('apps.order.api.urls')),
#     path('api/', include('apps.cart.api.urls')),


#     # path('api/coupon/', include('apps.coupon.api.urls')),
#     # path('api/newsletter/', include('apps.newsletter.api.urls')),

#     # path('api/checkout/', include('apps.order.api.urls')),
#     # path('api/cart/', include('apps.cart.api.urls')),
#     # path('api/cart/add/<int:product_id>/', include('apps.cart.api.urls')),
#     # path('api/cart/remove/<int:product_id>/', include('apps.cart.api.urls')),
#     # path('api/cart/detail/', include('apps.cart.api.urls')),
#     # path('api/cart/success/', include('apps.cart.api.urls')),
#     # path('api/webhook/', include('apps.cart.api.urls')),

#     # Store
#     path('api/', include('apps.store.api.urls')),


#     # path('api/search/', include('apps.store.api.urls')),
#     # path('api/variations/', include('apps.store.api.urls')),
#     # path('api/options/', include('apps.store.api.urls')),
#     # path('api/specifications/', include('apps.store.api.urls')),
#     # path('api/products/<str:category_slug>/<str:slug>/', include('apps.store.api.urls')),
#     # path('api/categories/<str:slug>/', include('apps.store.api.urls')),
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # path('', frontpage, name='frontpage'),
    # path('cart/', cart_detail, name='cart'),
    # path('hooks/', webhook, name='webhook'),
    # path('cart/success/', success, name='success'),
    # path('contact/', contact, name='contact'),
    # path('about/', about, name='about'),
    # path('admin/', admin.site.urls),
    # path('admin/admin_order_pdf/<int:order_id>/', admin_order_pdf, name='admin_order_pdf'),

    # # Auth

    # path('myaccount/', myaccount, name='myaccount'),
    # path('signup/', signup, name='signup'),
    # path('login/', views.LoginView.as_view(template_name='login.html'), name='login'),
    # path('logout/', views.LogoutView.as_view(), name='logout'),
    # path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    # # API

    # path('api/can_use/', api_can_use, name='api_can_use'),
    # path('api/create_checkout_session/', create_checkout_session, name='create_checkout_session'),
    # path('api/add_to_cart/', api_add_to_cart, name='api_add_to_cart'),
    # path('api/remove_from_cart/', api_remove_from_cart, name='api_remove_from_cart'),
    # path('api/add_subscriber/', api_add_subscriber, name='api_add_subscriber'),

    # path('search/', search, name='search'),
    # path('<slug:category_slug>/<slug:slug>/', product_detail, name='product_detail'),
    # path('<slug:slug>/', category_detail, name='category_detail'),