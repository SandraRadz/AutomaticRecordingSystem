from django.urls import path
from methodist.views import MethodistListView


urlpatterns = [
    path('<slug:user_id>', MethodistListView.as_view())
]