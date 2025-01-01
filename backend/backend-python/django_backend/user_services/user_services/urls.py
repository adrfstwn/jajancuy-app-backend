"""
URL configuration for user_services project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from accounts_managements.views import (Register, Login, GoogleLogin, ResetPassword, 
                                        ForgotPassword, UserProfile, EditUserProfile)

urlpatterns = [
    
    # ADMIN SITE
    path('admin/', admin.site.urls),
    
    # TOKEN JWT CLAIM
    path('api/token', TokenObtainPairView.as_view(), name='token_obtain'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    
    # ACCOUNTS SSO MANAGEMENT
    path('auth/signup', Register.as_view(), name='register'),
    path('auth/login', Login.as_view(), name='login'),
    path('auth/google/login', GoogleLogin.as_view(), name='google_login'),
    path('auth/user', UserProfile.as_view(), name='info_user'),
    path('auth/user/edit', EditUserProfile.as_view(), name='edit_info_user'),
    
    path('forgot-password', ForgotPassword.as_view(), name='forgot_password'),
    path('reset-password/<str:uidb64>/<str:token>', ResetPassword.as_view(), name='reset_passwrod'),
    
    
    
    # # AUTH SSO
    # path('accounts/', include('allauth.urls')),
]
