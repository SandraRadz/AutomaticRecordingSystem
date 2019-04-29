from plan.views import PlanListView
from django.urls import path

urlpatterns = [
    path('', PlanListView.as_view())
]
