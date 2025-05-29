from django.urls import path
from api_v1.views import TaskDetailUpdateDeleteView, TaskListCreateView


urlpatterns = [
    path("<int:pk>/", TaskDetailUpdateDeleteView.as_view(), name="task_detail"),
    path("", TaskListCreateView.as_view(), name="task_list"),
]
