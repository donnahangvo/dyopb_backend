from django.urls import path
from apps.userprofile.api.views import signup_view, logout_view, myaccount
from rest_framework.authtoken.views import obtain_auth_token

# app_name = 'userprofile'

urlpatterns = [
    path('myaccount', myaccount, name="myaccount"),
    path('signup', signup_view, name="signup"),
    path('login', obtain_auth_token, name="login"),
    path('logout', logout_view, name="logout"),
]