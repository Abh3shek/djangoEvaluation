from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'user', 'app', 'screenshot', 'completed', 'created_at']
        read_only_fields = ['id', 'created_at', 'user']

    def create(self, validated_data):
        # Automatically associate the logged-in user with the task
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)
