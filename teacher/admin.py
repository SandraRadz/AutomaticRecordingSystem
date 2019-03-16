from django.contrib import admin
from teacher.models import *

# Register your models here.
admin.site.register(Faculty)
admin.site.register(Department)
admin.site.register(Teacher)
admin.site.register(CountOfHour)
admin.site.register(Specialty)
admin.site.register(StudentGroup)

