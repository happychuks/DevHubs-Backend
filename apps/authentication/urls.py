from django.urls import path
from .views import SignupView, LoginView, LogoutView, PasswordResetView, PasswordResetConfirmView, GoogleLogin, GitHubLogin

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password-reset/', PasswordResetView.as_view(), name='password-reset'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    
    # OAuth URLs
    path('google-login/', GoogleLogin.as_view(), name='google_login'),
    path('github-login/', GitHubLogin.as_view(), name='github_login'),
]
