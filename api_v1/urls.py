from django.urls import path
from rest_framework import routers

from api_v1.views import TaskDetailView, TaskListView


urlpatterns = [
    path('<int:pk>', TaskDetailView.as_view(), name='task-detail'),
    path('', TaskListView.as_view(), name='task-list'),
]
