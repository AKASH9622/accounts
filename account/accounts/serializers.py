from rest_framework_simplejwt.backends import TokenBackend
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenVerifySerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from rest_framework import serializers

from django.contrib.auth.hashers import make_password

from django.contrib.auth import authenticate

User = get_user_model()

# Login

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    platform = serializers.CharField(write_only=True)

    def validate(self, attrs):
        platform = attrs.get('platform').lower()
        email = attrs.get('email')
        password = attrs.get('password', None)

        if platform == 'email':
            # Perform the normal email/password authentication
            user = authenticate(username=email, password=password)
            if not user:
                raise serializers.ValidationError({'error': 'Invalid credentials for email authentication.','detail':'No active account found with the given credentials'})
        else:
            # Handle OAuth authentication (Google, Facebook, etc.)
            try:
                user = User.objects.get(email=email, platform__iexact=platform)
            except User.DoesNotExist:
                raise serializers.ValidationError({'error': 'User does not exist for this platform.','detail':'No active account found with the given credentials'})

        if user is not None:
            if not user.is_active:
                raise serializers.ValidationError({'error': 'User account is disabled.','detail':'No active account found with the given credentials'})
            
            # Create a manual token since we bypass super().validate(attrs)
            refresh = RefreshToken.for_user(user)

            data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'id': user.id,
                'email': user.email,
                'roles': user.get_permissions,
            }

            # Add profile check
            vendor_profile_check = user.check_vendor_profile
            if vendor_profile_check:
                data.update({'profile': vendor_profile_check})
            else:
                client_profile_check = user.check_client_profile
                if client_profile_check:
                    data.update({'profile': client_profile_check})
                else:
                    data.update({'profile': {}})

            return data

        raise serializers.ValidationError({'error': 'Authentication failed.','detail':'No active account found with the given credentials'})

class CustomTokenVerifySerializer(TokenVerifySerializer):
    def validate(self,attrs):
        # The default result (access/refresh tokens)

        data = super(CustomTokenVerifySerializer, self).validate(attrs)

        # Custom data you want to include
        valid_data = TokenBackend(algorithm='HS256').decode(attrs['token'],verify=False)

        user = User.objects.get(id=valid_data['user_id'])

        # User Model
        data.update({'id':user.id})
        data.update({'email':user.email})
        # data.update({'first_name':user.first_name})
        # data.update({'last_name':user.last_name})
        # data.update({'phone_number':user.last_name})
        # data.update({'email_verify':user.email_verify})
        data.update({'roles':user.get_permissions})

        # and everything else you want to send in the response
        return data

# Signup / Register
from rest_framework import serializers
from .models import User, Role

from rest_framework_simplejwt.tokens import RefreshToken

class SignupSerializer(serializers.ModelSerializer):
    roles = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), many=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone_number', 'roles', 'password']

    def create(self, validated_data):
        # Hash the password before saving the user
        validated_data['password'] = make_password(validated_data['password'])

        # Create the user
        user = super().create(validated_data)

        # Generate tokens
        tokens = self.generate_tokens(user)

        # Include tokens in the response
        response_data = self.data
        response_data['access_token'] = tokens['access']
        response_data['refresh_token'] = tokens['refresh']

        return response_data

    def generate_tokens(self, user):
        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)

        return {'access': access, 'refresh': str(refresh)}

class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone_number']

# Password
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

# Utils
from .models import countries, states, cities

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = countries
        fields = ['id', 'name', 'shortname', 'phonecode']

class StateSerializer(serializers.ModelSerializer):
    country = serializers.CharField(source='country_id.name')

    class Meta:
        model = states
        fields = ['id', 'name', 'country']

class CitiesSerializer(serializers.ModelSerializer):
    state = serializers.CharField(source='state_id.name')

    class Meta:
        model = cities
        fields = ['id', 'name', 'state']

class CountryWithStatesSerializer(serializers.ModelSerializer):
    states = StateSerializer(many=True, read_only=True, source='states_set')

    class Meta:
        model = countries
        fields = ['id', 'name', 'shortname', 'phonecode', 'states']