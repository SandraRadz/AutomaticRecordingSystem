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


class Specialty(models.Model):
    specialty_name = models.CharField(max_length=250, unique=True)
    # TO DO how it must look like?
    code = models.CharField(max_length=10)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, to_field='department_name')

    def __str__(self):
        return self.specialty_name


class StudentGroup(models.Model):
    id = models.AutoField(primary_key=True)
    year_of_entry = models.SmallIntegerField()
    first_deadline_date = models.DateField(null=True, blank=True)
    last_deadline_date = models.DateField(null=True, blank=True)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, to_field='specialty_name')


class BranchOfKnowledge(models.Model):
    branch_name = models.CharField(max_length=100, unique=True)
    wider_branch = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.branch_name


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
    branch = models.ManyToManyField(BranchOfKnowledge)

    def __str__(self):
        return self.teacher_name


class CountOfHour(models.Model):
    id = models.AutoField(primary_key=True)
    count_of_themes = models.SmallIntegerField()
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, to_field='teacher_name')
    specialty = models.ForeignKey(StudentGroup, on_delete=models.CASCADE)
