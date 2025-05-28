from django.contrib import admin
from .models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'completed']
    list_filter = ['completed']
    search_fields = ['title', 'description']
    fields = ['title', 'description', 'completed', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']


admin.site.register(Task, TaskAdmin)
