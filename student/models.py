from django.db import models
from teacher.models import Department


# Create your models here.
class Specialty(models.Model):
    specialty_name = models.CharField(max_length=250, unique=True)
    # TO DO how it must look like?
    code = models.CharField(max_length=10, unique=True)
    # TO DO Will it be better if we create list of years?.
    year_of_entry = models.SmallIntegerField()
    first_deadline_date = models.DateField(null=True, blank=True)
    last_deadline_date = models.DateField(null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, to_field='department_name')

    def __str__(self):
        return self.specialty_name


class Student(models.Model):
    student_name = models.CharField(max_length=35, unique=True)
    office_365_email = models.EmailField()
    additional_email = models.EmailField(null=True, blank=True)
    average_mark = models.FloatField(null=True, blank=True)
    # TO DO write more information
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, to_field='specialty_name')

    def __str__(self):
        return self.student_name
