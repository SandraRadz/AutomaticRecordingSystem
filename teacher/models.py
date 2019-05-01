import datetime

from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Faculty(models.Model):
    faculty_name = models.CharField(max_length=250, unique=True)
    dean = models.CharField(max_length=250)
    dean_contact = models.TextField(null=True, blank=True)
    dean_office = models.CharField(max_length=250, null=True, blank=True)
    deanery_contact = models.TextField(null=True, blank=True)
    deanery_office = models.CharField(max_length=250, null=True, blank=True)
    faculty_methodist = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return self.faculty_name


class Department(models.Model):
    department_name = models.CharField(max_length=250, unique=True)
    head_of_department = models.CharField(max_length=250)
    office = models.CharField(max_length=250, null=True, blank=True)
    phone = models.CharField(max_length=250, null=True, blank=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)

    def __str__(self):
        return self.department_name


class Specialty(models.Model):
    specialty_name = models.CharField(max_length=250, unique=True)
    specialty_standard_name = models.CharField(max_length=250, unique=True, null=True, blank=True)
    specialty_code = models.SmallIntegerField()
    branch_code = models.SmallIntegerField()
    branch_name = models.CharField(max_length=250, unique=True, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.specialty_name


class StudentGroup(models.Model):
    # we need id there to choose groups id in student table
    id = models.AutoField(primary_key=True)
    year_of_entry = models.SmallIntegerField()
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE)


class Protection(models.Model):
    speciality_group = models.ForeignKey(StudentGroup, on_delete=models.CASCADE)
    teacher_department = models.ForeignKey(Department, on_delete=models.CASCADE)
    date_of_pre_protection = models.DateTimeField(null=True, blank=True)
    date_of_confirmation = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.student + self.work


class BranchOfKnowledge(models.Model):
    branch_name = models.CharField(max_length=100, unique=True)
    wider_branch = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.branch_name


class Teacher(models.Model):
    teacher_id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    degree = models.CharField(max_length=50, null=True, blank=True)
    position = models.CharField(max_length=50)
    academic_status = models.CharField(max_length=50, null=True, blank=True)
    office = models.CharField(max_length=250, null=True, blank=True)
    phone = models.CharField(max_length=250, null=True, blank=True)
    additional_email = models.EmailField(null=True, blank=True)
    send_email = models.BooleanField(default=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    branch = models.ManyToManyField(BranchOfKnowledge, blank=True)

    def __str__(self):
        return str(self.teacher_id)


class TopicOffer(models.Model):
    id = models.AutoField(primary_key=True)
    count_of_themes = models.SmallIntegerField()
    fact_count_of_themes = models.SmallIntegerField(default=0)
    year_of_study = models.SmallIntegerField()
    year_of_work = models.SmallIntegerField(default=datetime.date.today().year)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    specialty = models.ForeignKey(StudentGroup, on_delete=models.CASCADE)

    def __str__(self):
        return self.teacher.teacher_id.first_name + " " + self.specialty.specialty.specialty_name + " - " + \
               str(self.year_of_study) + " = " + str(self.fact_count_of_themes)+"/" + str(self.count_of_themes)


class CountOfWork(models.Model):
    degree = models.CharField(max_length=50, null=True, blank=True)
    academic_status = models.CharField(max_length=50, null=True, blank=True)
    count_of_course_work = models.SmallIntegerField()
    count_of_qualification_work = models.SmallIntegerField()
