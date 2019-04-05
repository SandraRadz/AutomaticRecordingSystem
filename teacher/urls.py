from django.conf.urls import url

from teacher.views import  TeacherListView
from . import views
from django.urls import path

urlpatterns = [
    path('', TeacherListView.as_view())
]