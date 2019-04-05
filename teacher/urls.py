from teacher.views import TeacherListView
from django.urls import path

urlpatterns = [
    path('', TeacherListView.as_view())
]