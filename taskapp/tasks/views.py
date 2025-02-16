from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from .models import Task
from .serializers import TaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Regular users see only their tasks; admins can see all tasks if needed
        user = self.request.user
        if user.is_staff:
            return Task.objects.all()
        return Task.objects.filter(user=user)
