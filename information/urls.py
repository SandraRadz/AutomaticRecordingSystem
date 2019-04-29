from django.urls import path

from information.views import InfoListView
from . import views

urlpatterns = [
    path('', InfoListView.as_view())
]