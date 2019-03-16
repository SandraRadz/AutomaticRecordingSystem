from django.db import models

# Create your models here.
from theme.models import WriteWork


class Plan(models.Model):
    deadline = models.DateTimeField()
    description = models.TextField()
    work_name = models.ForeignKey(WriteWork, on_delete=models.CASCADE, to_field='work_name')
