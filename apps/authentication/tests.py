from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

class AuthenticationTests(APITestCase):

    def test_user_registration(self):
        url = reverse('register')
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpass123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_google_login(self):
        url = reverse('google_login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_github_login(self):
        url = reverse('github_login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
