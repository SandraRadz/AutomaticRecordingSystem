from django.urls import path
from deadline.views import DeadlineListView


urlpatterns = [
    path('', DeadlineListView.as_view())
]