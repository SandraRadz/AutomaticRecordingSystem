from django.db import models

# Create your models here.
class Teacher(models.Model):
    lastName = models.CharField(max_length=35)
    firstName = models.CharField(max_length=35)
    secondName = models.CharField(max_length=35)

    