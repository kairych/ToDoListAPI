from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from api_v1.serializers import TaskSerializer
from to_do_app.models import Task


class TaskViewSet(viewsets.ModelViewSet):
    """API endpoint that allows tasks to be viewed or edited."""
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated,]
