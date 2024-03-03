# from rest_framework import serializers
# from djoser.serializers import UserCreateSerializer, UserSerializer
# from .models import UserProfile

# class UserProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserProfile
#         fields = '__all__'

# class CustomUserCreateSerializer(UserCreateSerializer):
#     profile = UserProfileSerializer(required=False)

#     class Meta(UserCreateSerializer.Meta):
#         fields = UserCreateSerializer.Meta.fields + ('profile',)

#     def create(self, validated_data):
#         profile_data = validated_data.pop('profile', None)
#         user = super().create(validated_data)
#         if profile_data:
#             UserProfile.objects.create(user=user, **profile_data)
#         return user

# class CustomUserSerializer(UserSerializer):
#     profile = UserProfileSerializer(required=False)

#     class Meta(UserSerializer.Meta):
#         fields = UserSerializer.Meta.fields + ('profile',)