from teacher import views
from teacher.views import TeacherListView, createTheme
from django.urls import path

urlpatterns = [
    path('new_theme', createTheme),
    path('new_theme/<str:spec>', createTheme),
    path('<slug:user_id>', TeacherListView.as_view())
]
