from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect


# Create your views here.
def index(request):
    if 'mail' not in request.session:
        return HttpResponseRedirect('../authorization/')
    return render(request, 'plans/plans.html')
