from django.urls import path
from methodist.views import MethodistListView


urlpatterns = [
    path('', MethodistListView.as_view())
]