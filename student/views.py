from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.views.generic import DetailView

from student.models import Student


def index(request):
    if 'mail' not in request.session:
        return HttpResponseRedirect('../authorization/')
    return HttpResponse('<h1>Student page</h1>')


class StudentDetailView(DetailView):
    template_name = 'teacher/student.html'
    model = Student

    def get(self, *args, **kwargs):
        if 'mail' not in self.request.session:
            return HttpResponseRedirect('../authorization/')
        if 'role' != 'student':
            return HttpResponseRedirect('../authorization/')
        return super(StudentDetailView, self).get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
