from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from .models import AndroidApp
from .serializers import AndroidAppSerializer

# Custom permission to allow only admin users (is_staff) to create/update/delete
class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)

class AndroidAppViewSet(viewsets.ModelViewSet):
    queryset = AndroidApp.objects.all()
    serializer_class = AndroidAppSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated, IsAdmin]
        else:
            # For list/retrieve, any authenticated user can see the apps
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
