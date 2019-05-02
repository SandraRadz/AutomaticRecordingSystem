from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from teacher.models import Department
from teacher.models import StudentGroup


class Student(models.Model):
    student_id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    average_mark = models.FloatField(null=True, blank=True)
    additional_email = models.EmailField(null=True, blank=True)
    send_email = models.BooleanField(default=True)
    specialty = models.ForeignKey(StudentGroup, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.student_id.first_name)
