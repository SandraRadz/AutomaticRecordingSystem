from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView

# Create your views here.
from plan.models import Plan


def index(request):
    if 'mail' not in request.session:
        return HttpResponseRedirect('../authorization/')
    return render(request, 'plans/plans.html')


class PlanListView(ListView):
    template_name = 'plans/plans.html'
    model = Plan

    def get(self, *args, **kwargs):
        if 'mail' not in self.request.session:
            return HttpResponseRedirect('../authorization/')
        return super(PlanListView, self).get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PlanListView, self).get_context_data(**kwargs)
        context['plan'] = Plan.objects.all()
        return context
