# CODE GRAVEYARD
# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.decorators import api_view

# from serializers import 


# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import AllowAny
# from rest_framework.response import Response
# from djoser.views import UserViewSet

# @api_view(['POST'])
# @permission_classes([AllowAny])
# def signup(request):
#     return UserViewSet.as_view({'post': 'create'})(request)

# @api_view(['POST'])
# @permission_classes([AllowAny])
# def user_login(request):
#     return UserViewSet.as_view({'post': 'login'})(request)

# @api_view(['POST'])
# def user_logout(request):
#     return UserViewSet.as_view({'post': 'logout'})(request)


# from rest_framework import status
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from django.contrib.auth import authenticate, login, logout
# from serializers import UserProfileSerializer
# # from django.contrib.auth.models import User
# from forms import SignUpForm, UserProfileForm

# @api_view(['POST'])
# def signup(request):
#     if request.method == 'POST':
#         user_serializer = SignUpForm(data=request.data)
#         profile_serializer = UserProfileForm(data=request.data)

#         if user_serializer.is_valid() and profile_serializer.is_valid():
#             user = user_serializer.save()
#             profile = profile_serializer.save(user=user)
#             return Response({'message': 'New user created successfully'}, status=status.HTTP_201_CREATED)
#         return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST'])
# def signup_view(request):

#     if request.method == 'POST':
#         serializer = SignUpSerializer(data=request.data)
#         data = {}
#         if serializer.is_valid():
#             account = serializer.save()
#             data['response'] = 'New user successfully registered.'
#             data['email'] = account.email
#             data['username'] = account.username
#             token = Token.objects.get(user=account).key
#             data['token'] = token
#         else:
#             data = serializer.errors
#         return Response(data)
    

# @api_view(['POST'])
# def user_login(request):
#     if request.method == 'POST':
#         username = request.data.get('username')
#         password = request.data.get('password')
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
#         else:
#             return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# @api_view(['POST'])
# def user_logout(request):
#     if request.method == 'POST':
#         logout(request)
#         return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)



# from django.shortcuts import render, redirect
# from django.contrib.auth import login
# from django.contrib.auth.decorators import login_required

# from .forms import SignUpForm, UserProfileForm

# def signup(request):
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         userprofileform = UserProfileForm(request.POST)

#         if form.is_valid() and userprofileform.is_valid():
#             user = form.save()

#             userprofile = userprofileform.save(commit=False)
#             userprofile.user = user
#             userprofile.save()

#             login(request, user)

#             return redirect('frontpage')
#     else:
#         form = SignUpForm()
#         userprofileform = UserProfileForm()
    
#     return render(request, 'signup.html', {'form': form, 'userprofileform': userprofileform})

# @login_required
# def myaccount(request):
#     return render(request, 'myaccount.html')