from teacher import views
from teacher.views import TeacherListView, createTheme
from django.urls import path

urlpatterns = [
    path('', TeacherListView.as_view()),
    path('new_theme', createTheme)
]