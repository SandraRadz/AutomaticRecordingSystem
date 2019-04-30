import datetime

from django.db import models

# Create your models here.
from student.models import Student
from teacher.models import TopicOffer
from teacher.models import BranchOfKnowledge


class WriteWork(models.Model):
    work_name = models.CharField(max_length=500)
    english_work_name = models.CharField(max_length=500, null=True, blank=True)
    year_of_work = models.SmallIntegerField(default=datetime.date.today().year)
    note = models.TextField(null=True, blank=True)
    student = models.ManyToManyField(Student, through='Record', blank=True)
    previous_version = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    branch = models.ManyToManyField(BranchOfKnowledge, blank=True)
    teacher_offer = models.ForeignKey(TopicOffer, on_delete=models.CASCADE)

    def __str__(self):
        return self.work_name


class Record(models.Model):
    STATUS_TITLE = (
        ('WAIT', 'очікується підтвердження'),
        ('CONFIRMED', 'підтверджкно викладачем'),
        ('REJECTED', 'відхилено викладачем'),
        ('BLOCKED', 'затверджено на іншу тему')
    )
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    work = models.ForeignKey(WriteWork, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_TITLE)
    date_of_record = models.DateTimeField(auto_now_add=True)
    date_of_confirmation = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.student.student_id.username + ' - ' + self.work.work_name



