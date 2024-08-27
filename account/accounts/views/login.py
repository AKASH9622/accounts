from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView
from django.contrib.auth import get_user_model

from accounts import serializers

from django.conf import settings

User = get_user_model()

# Custom Authentication
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = serializers.CustomTokenObtainPairSerializer


class CustomTokenVerify(TokenVerifyView):
    serializer_class = serializers.CustomTokenVerifySerializer
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        return response