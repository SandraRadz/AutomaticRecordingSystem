from django.db import models


# Create your models here.
from teacher.models import Department
from teacher.models import StudentGroup


class Student(models.Model):
    student_name = models.CharField(max_length=35, unique=True)
    office_365_email = models.EmailField(unique=True)
    additional_email = models.EmailField(null=True, blank=True)
    average_mark = models.FloatField(null=True, blank=True)
    # TO DO write more information
    specialty = models.ForeignKey(StudentGroup, on_delete=models.CASCADE)

    def __str__(self):
        return self.student_name
