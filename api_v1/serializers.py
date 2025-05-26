from rest_framework import serializers
from to_do_app.models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description', 'completed', 'created_at', 'updated_at']
        read_only = ['id', 'created_at', 'updated_at']