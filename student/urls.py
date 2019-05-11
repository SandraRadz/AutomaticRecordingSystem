from student.views import StudentListView
from django.urls import path

urlpatterns = [
    path('<slug:user_id>', StudentListView.as_view())
]
