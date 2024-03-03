from django.urls import path
from apps.newsletter.api.views import add_subscriber

urlpatterns = [
    path('newsletter', add_subscriber, name='newsletter'),
]