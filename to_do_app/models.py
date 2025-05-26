from django.db import models


class Task(models.Model):
    title = models.CharField(max_length=200, verbose_name="Title")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    completed = models.BooleanField(default=False, verbose_name="Completed")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At", null=True, blank=True)

    def __str__(self):
        return f"{self.title[:25]}"
