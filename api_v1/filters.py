from django_filters import FilterSet, CharFilter, BooleanFilter
from to_do_app.models import Task

class TaskFilter(FilterSet):
    title = CharFilter(lookup_expr='icontains')
    completed = BooleanFilter()

    class Meta:
        model = Task
        fields = ['completed', 'title']
