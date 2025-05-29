from rest_framework import serializers
from to_do_app.models import Task, AstanaHub


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description', 'completed', 'created_at', 'updated_at']
        read_only = ['id', 'created_at', 'updated_at']


class AstanaHubSerializer(serializers.ModelSerializer):
    class Meta:
        model = AstanaHub
        fields = '__all__'
        read_only = ['id', 'created_at', 'updated_at']
