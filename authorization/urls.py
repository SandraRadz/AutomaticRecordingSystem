from django.contrib import admin
from django.urls import path
from django.urls import include
from authorization import views

app_name = 'authorization'
urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('gettoken', views.gettoken, name='gettoken'),
]