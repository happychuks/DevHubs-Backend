from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from allauth.socialaccount.models import SocialAccount
from .models import CustomUser

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model to serialize user details.
    """
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'bio', 'profile_picture']
        read_only_fields = ['id']

class SignupSerializer(serializers.ModelSerializer):
    """
    Serializer for user signup, including password validation.
    """
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'bio', 'profile_picture']
        extra_kwargs = {
            'password': {'write_only': True},
            'bio': {'required': False},
            'profile_picture': {'required': False}
        }

    def validate_password(self, value):
        """
        Validate the password using Django's built-in validators.
        """
        validate_password(value)
        return value

    def create(self, validated_data):
        """
        Create a new user instance and hash the password.
        """
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            bio=validated_data.get('bio', ''),
            profile_picture=validated_data.get('profile_picture', '')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    username_or_email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username_or_email = data.get('username_or_email')
        password = data.get('password')

        user = None
        if User.objects.filter(username=username_or_email).exists():
            user = authenticate(username=username_or_email, password=password)
        elif User.objects.filter(email=username_or_email).exists():
            user = authenticate(email=username_or_email, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid login credentials.")
        if not user.is_active:
            raise serializers.ValidationError("User account is disabled.")
        data['user'] = user
        return data
    
class PasswordResetSerializer(serializers.Serializer):
    """
    Serializer for password reset request, accepting an email address.
    """
    email = serializers.EmailField()

class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Serializer for password reset confirmation, checking if new passwords match.
    """
    new_password = serializers.CharField(write_only=True)
    re_new_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        """
        Check if both new password fields match.
        """
        if attrs['new_password'] != attrs['re_new_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return attrs

class SocialAccountSerializer(serializers.ModelSerializer):
    """
    Serializer for SocialAccount model to serialize social account details.
    """
    class Meta:
        model = SocialAccount
        fields = ['provider', 'uid', 'last_login', 'date_joined']
