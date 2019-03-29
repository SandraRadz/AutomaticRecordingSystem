from django.conf.urls import url
from django.urls import path
from theme.views import *

app_name = 'theme'

urlpatterns = [
    path('', ThemeListView.as_view())
]