from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import MethodNotAllowed

from apps.userprofile.api.serializers import UserProfileSerializer, SignUpSerializer


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def myaccount(request):
    user = request.user

    if request.method == 'GET':
        # Retrieve and serialize the user's account data
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        # Update the user's account data
        serializer = UserProfileSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {'success': 'Update successful'}
            return Response(data=data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # If the request method is neither GET nor PUT, return Method Not Allowed
    raise MethodNotAllowed(request.method)


@api_view(['POST'])
def signup_view(request):
    if request.method == 'POST':
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            # Save the user account
            account = serializer.save()

            # Generate and retrieve the authentication token
            token, _ = Token.objects.get_or_create(user=account)

            # Construct the response data
            data = {
                'response': 'New user successfully registered.',
                'email': account.email,
                'username': account.username,
                'token': token.key  # Include the token in the response
            }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            # Construct the error response
            data = {
                'errors': serializer.errors
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def logout_view(request):
    try:
        # Invalidate or delete the user's authentication token
        # Example with Django Rest Framework's TokenAuthentication
        request.user.auth_token.delete()
        return Response({"message": "Logged out successfully."}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)















# @api_view(['GET'])
# def myaccount(request):
    

# @api_view(['POST'])
# def signup_view(request):
#     if request.method == 'POST':
#         serializer = SignUpSerializer(data=request.data)
#         data = {}

#         if serializer.is_valid():
#             account = serializer.save()
#             data['response'] = "New user has successfully been created!"
#             data['email'] = account.email
#             data['username'] = account.username
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