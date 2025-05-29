from django.db import models


class Task(models.Model):
    title = models.CharField(max_length=200, verbose_name="Title")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    completed = models.BooleanField(default=False, verbose_name="Completed")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At", null=True, blank=True)

    def __str__(self):
        return f"{self.title[:25]}"


class AstanaHub(models.Model):
    cert_number = models.CharField(max_length=10, verbose_name="Certificate Number")
    cert_issue_date = models.DateField(verbose_name="Certificate Issue Date")
    cert_expire_date = models.DateField(verbose_name="Certificate Expire Date")
    bin = models.CharField(max_length=12, verbose_name="BIN")
    is_active = models.BooleanField(default=False, verbose_name="Active")
    company_name = models.CharField(max_length=100, verbose_name="Company Name")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At", null=True, blank=True)

