from student.views import StudentListView
from django.urls import path

urlpatterns = [
    path('', StudentListView.as_view())
]
