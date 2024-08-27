from django.urls import path, include, re_path

#JWT
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from . import views

app_name = "accounts"

jwtpatterns = [
    path('', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify/', views.CustomTokenVerify.as_view(), name='token_verify'),
]

urlpatterns = [
    #JWT Urls
    path('auth/',include(jwtpatterns)),

    path('check/', views.email_check, name='email_check'),
    
    #Profile Urls
    path('signup/', views.Signup.as_view(), name='signup'),
    path('update-profile/<int:pk>/', views.UpdateProfile.as_view(), name='update-profile'),
    path('change-password/', views.ChangePassword.as_view(), name='change-password'),
    path('reset-password/', views.PasswordResetRequest.as_view(), name='reset-password'),
    path('reset-password/verify_token/', views.FirstVerifyPasswordResetOTP.as_view(), name='verify-token'),
    path('reset-password/verify/', views.VerifyPasswordResetOTP.as_view(), name='verify-password'),

    #Utils
    path('common/', views.common_template, name='common_template'),
    path('countries/', views.get_countries, name='get_countries'),
    path('states/', views.get_states, name='get_states'),
    path('cities/', views.get_cities, name='get_cities'),
]
