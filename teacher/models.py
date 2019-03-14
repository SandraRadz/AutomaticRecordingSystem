from django.db import models


# Create your models here.
class Faculty(models.Model):
    faculty_name = models.CharField(max_length=250, unique=True)
    dean = models.CharField(max_length=250)

    # TO DO write more information

    def __str__(self):
        return self.faculty_name


class Department(models.Model):
    department_name = models.CharField(max_length=250, unique=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, to_field='faculty_name')

    # TO DO write more information

    def __str__(self):
        return self.department_name


class Teacher(models.Model):
    teacher_name = models.CharField(max_length=35, unique=True)
    office_365_email = models.EmailField()
    additional_email = models.EmailField(null=True, blank=True)
    degree = models.CharField(max_length=50, null=True, blank=True)
    # TO DO write more information
    # naukovuy stypin
    # posada
    office = models.CharField(max_length=250, null=True, blank=True)
    phone = models.CharField(max_length=250, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, to_field='department_name')

    def __str__(self):
        return self.teacher_name
