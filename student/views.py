from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
def index(request):
    if 'mail' not in request.session:
        return HttpResponseRedirect('../authorization/')
    return HttpResponse('<h1>Student page</h1>')

