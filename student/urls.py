from django.conf.urls import url

from student.views import  StudentListView
from . import views
from django.urls import path

urlpatterns = [
    path('', StudentListView.as_view())
]