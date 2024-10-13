from rest_framework_simplejwt.tokens import Token
from .models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from allauth.socialaccount.models import SocialAccount

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class MyTOPS(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        """
        Dictionary that holds the user's information
        """
        token = super().get_token(user)

        if hasattr(user, 'profile'):
            token['full_name'] = user.profile.full_name
            token['bio'] = user.profile.bio
        token['username'] = user.username
        token['email'] = user.email

        return token

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    full_name = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['full_name', 'email', 'username', 'password', 'password2']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {'password':"Password Fields Didn't Match"}
            )
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()

        if "full_name" in validated_data and hasattr(user, 'profile'):
            user.profile.full_name = validated_data['full_name']
            user.profile.save()

        return user

class SocialAccountSerializer(serializers.ModelSerializer):
    """
    Serializer for SocialAccount model to serialize social account details.
    """
    class Meta:
        model = SocialAccount
        fields = ['provider', 'uid', 'last_login', 'date_joined']