from rest_framework import generics
from rest_framework import permissions

from django.conf import settings

from ..models import User
from ..serializers import SignupSerializer, UpdateProfileSerializer, ChangePasswordSerializer, PasswordResetSerializer
from ..permissions import IsOwnerOrAdmin

from accounts.Utils import Util

import random
from django.core.cache import cache

def generate_otp():
    return str(random.randint(1000, 9999))

import base64
import json
from urllib.parse import quote, unquote

def encode_email_otp(email, otp):
    data = json.dumps({'email': email, 'otp': otp})
    token = base64.urlsafe_b64encode(data.encode()).decode()
    return quote(token)

def decode_email_otp(token):
    decoded_data = base64.urlsafe_b64decode(unquote(token)).decode()
    return json.loads(decoded_data)

class Signup(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignupSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.save()

        return Response(data, status=status.HTTP_201_CREATED)

class UpdateProfile(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UpdateProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        # Add partial=True to allow partial updates
        kwargs['partial'] = True
        return super().get_serializer(*args, **kwargs)

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import update_session_auth_hash

class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            # Check if the old password matches
            if not request.user.check_password(serializer.validated_data.get('old_password')):
                return Response({'error': 'Invalid old password.'}, status=status.HTTP_400_BAD_REQUEST)

            # Set the new password
            request.user.set_password(serializer.validated_data.get('new_password'))
            request.user.save()

            # Update the session auth hash
            update_session_auth_hash(request, request.user)

            return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
from django.core.cache import cache
from datetime import timedelta

class PasswordResetRequest(APIView):
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        # Check if email exists in the database
        if not User.objects.filter(email=email).exists():
            return Response({'detail': 'Email not found'}, status=status.HTTP_404_NOT_FOUND)

        # Generate OTP
        otp = generate_otp()

        # Set timeout for cache (15 minutes)
        timeout_minutes = 15
        timeout_seconds = timeout_minutes * 60

        # Store OTP in cache with 15-minute timeout
        cache.set(email, otp, timeout=timeout_seconds)

        # Prepare Verify Link
        token = encode_email_otp(email, otp)
        verification_link = f'https://proptrader.netlify.app/verify_otp?token={token}'

        # Prepare email content
        subject = 'Reset Password'
        message = f'Click the link to verify: {verification_link}'

        Util.send_email(subject, message, 'shyampopz0@gmail.com', email)

        return Response({'message': 'Mail sent successfully'}, status=status.HTTP_200_OK)

from django.contrib.auth.hashers import make_password

class FirstVerifyPasswordResetOTP(APIView):
    def post(self, request):
        token = request.data.get('token')

        try:
            data = decode_email_otp(token)
            email = data['email']
            otp_entered = data['otp']

            # Retrieve OTP from cache
            cached_otp = cache.get(email)

            if cached_otp is None:
                return Response({'message': 'OTP expired or invalid'}, status=status.HTTP_400_BAD_REQUEST)
            
            if otp_entered == cached_otp:
                return Response({'message': 'Token accepted successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)

        return Response({'error': 'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)


class VerifyPasswordResetOTP(APIView):
    def post(self, request):
        token = request.data.get('token')
        new_password = request.data.get('password')

        if new_password is None:
            return Response({'error': 'Password is required'}, status=status.HTTP_400_BAD_REQUEST)

        data = decode_email_otp(token)
        email = data['email']
        otp_entered = data['otp']

        # Retrieve OTP from cache
        cached_otp = cache.get(email)

        if cached_otp is None:
            return Response({'error': 'OTP expired or invalid'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Compare the entered OTP with the one retrieved from cache
        if otp_entered == cached_otp:
            
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

            # Update the user's password
            user.password = make_password(new_password)
            user.save()

            cache.delete(email)
            return Response({'message': 'Password updated successfully'}, status=status.HTTP_200_OK)
        
        return Response({'error': 'OTP expired or invalid'}, status=status.HTTP_400_BAD_REQUEST)
    
# Email verification
from rest_framework.decorators import api_view

@api_view(['POST'])
def email_check(request):
    data = request.data
    if User.objects.filter(email=data['email']).first():
        return Response({"error":"User with this email already exists"},status=status.HTTP_400_BAD_REQUEST)
    
    return Response(status=status.HTTP_200_OK)