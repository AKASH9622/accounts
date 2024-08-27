# views.py
from rest_framework import generics, permissions
from .models import User
from .serializers import UpdateProfileSerializer

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object or admin to update it.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the user is an admin
        if request.user.roles.filter(name='Admin').exists():
            return True
        # Check if the user is trying to update their own profile
        return obj == request.user
