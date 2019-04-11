from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from teacher.models import Department


class Methodist(models.Model):
    methodist_id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    additional_email = models.EmailField(null=True, blank=True)
    office = models.CharField(max_length=250)
    phone = models.CharField(max_length=250)
    send_email = models.BooleanField(default=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, to_field='department_name')

    def __str__(self):
        return str(self.methodist_id)

