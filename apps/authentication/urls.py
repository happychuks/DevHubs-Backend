from django.urls import path
from rest_framework_simplejwt.views import (TokenRefreshView)
from .views import MyTokenObtainPairView, RegisterView, protectedView, view_all_routes, GoogleLogin, GitHubLogin

urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(),name="token-obtain"),
    path('token/refresh/', TokenRefreshView.as_view(), name="refresh-token"),
    path('register/', RegisterView.as_view(), name="register-user"),
    path('test/', protectedView, name="test"),
    path('', view_all_routes, name="all-routes"),
    
    # OAuth URLs
    path('google-login/', GoogleLogin.as_view(), name='google_login'),
    path('github-login/', GitHubLogin.as_view(), name='github_login'),
]

"""
data = {
"email":"test@example.com",
"full_name":"Admin Test",
"username":"test",
"password":"pass12345",
"password2":"pass12345"
}
"""