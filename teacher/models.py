from django.db import models


# Create your models here.
class Faculty(models.Model):
    name = models.CharField(max_length=250, unique=True)
    dean = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=250, unique=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, to_field='name')

    def __str__(self):
        return self.name


class Teacher(models.Model):
    name = models.CharField(max_length=35, unique=True)
    office_365_email = models.EmailField()
    additional_email = models.EmailField(null=True, blank=True)
    degree = models.CharField(max_length=50, null=True, blank=True)
    # naukovuy stypin
    # posada
    office = models.CharField(max_length=250, null=True, blank=True)
    phone = models.CharField(max_length=250, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, to_field='name')

    def __str__(self):
        return self.name



