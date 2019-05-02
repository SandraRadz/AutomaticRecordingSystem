from django.db import models

# Create your models here.
from theme.models import WriteWork


class Plan(models.Model):
    deadline = models.DateTimeField(null=True, blank=True)
    description = models.TextField()
    work_name = models.ForeignKey(WriteWork, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.deadline)
