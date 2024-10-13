# users/tests.py
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient

User = get_user_model()

class UserTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword123',
            'roles': 'consumer',
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_user_registration(self):
        """Test user registration."""
        response = self.client.post(reverse('user-register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword123',
            'roles': 'developer',
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)  # Ensure user count increases

    def test_user_login(self):
        """Test user login."""
        response = self.client.post(reverse('user-login'), {
            'username': self.user.username,
            'password': self.user_data['password'],
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)  # Check for access token

    def test_user_login_invalid_credentials(self):
        """Test login with invalid credentials."""
        response = self.client.post(reverse('user-login'), {
            'username': self.user.username,
            'password': 'wrongpassword',
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_password_reset_request(self):
        """Test password reset request."""
        response = self.client.post(reverse('password-reset-request'), {
            'email': self.user.email,
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Password reset link has been sent.", response.data.values())
