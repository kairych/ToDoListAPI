from django.urls import path, include
from rest_framework import routers

from api_v1.views import TaskViewSet

router = routers.DefaultRouter()
router.register('tasks', TaskViewSet)

urlpatterns = [
    path('', include(router.urls)),
]