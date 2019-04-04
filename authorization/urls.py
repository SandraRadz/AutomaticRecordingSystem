from django.urls import path
from authorization import views

app_name = 'authorization'
urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('gettoken/', views.gettoken, name='gettoken'),
]