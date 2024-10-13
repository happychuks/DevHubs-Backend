from django.urls import reverse
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_str, force_bytes
from django.template.loader import render_to_string
from django.core.mail import send_mail
from .serializers import (
    UserSerializer,
    ProfileSerializer, ChangePasswordSerializer,
    PasswordResetSerializer, PasswordResetConfirmSerializer, 
    CustomTokenObtainPairSerializer
)
from .models import User
from django.conf import settings
import logging
logger = logging.getLogger(__name__)
User = get_user_model()

EMAIL_SUBJECT = "Password Reset Request"
FROM_EMAIL = settings.EMAIL_HOST_USER
TEMPLATE_PATH = 'emails/password_reset_email.html'

class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class UserLoginView(TokenObtainPairView):
    # This view provides the token pair (access and refresh)
    serializer_class = CustomTokenObtainPairSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Obtain tokens
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)
        
        return Response({
            'refresh': str(refresh),
            'access': access,
        })

class UserLogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)

class UserProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user.profile

class ChangePasswordView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)

class PasswordResetRequestView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)

        # Create password reset token
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        # Build the reset link dynamically
        link = request.build_absolute_uri(
            reverse('password-reset-confirm', kwargs={'uidb64': uid, 'token': token})
        )
        try:
            # Send password reset email
            html_message = render_to_string(TEMPLATE_PATH, {'username': user.username, 'link': link})       
            send_mail(subject="Password Reset", message="Password reset", html_message=html_message, from_email=settings.EMAIL_HOST_USER, recipient_list=['happychukwuma@gmail.com'], fail_silently=False)
            logger.info(f"Password reset email sent to {user.email}")
            return Response({"message": "Password reset link has been sent."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Failed to send password reset email."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class PasswordResetConfirmView(generics.GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request, uidb64, token):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

        if not default_token_generator.check_token(user, token):
            return Response({"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(serializer.validated_data['new_password1'])
        user.save()
        return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)
