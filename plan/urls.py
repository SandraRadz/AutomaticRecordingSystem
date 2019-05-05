from plan.views import PlanListView, PlanItemListView
from django.urls import path

urlpatterns = [
    path('', PlanListView.as_view()),
    path('<slug:plan_url>', PlanItemListView.as_view())
]
