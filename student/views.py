from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.views.generic import DetailView, ListView

from student.models import Student


def index(request):
    if 'mail' not in request.session:
        return HttpResponseRedirect('../authorization/')
    return HttpResponse('<h1>Student page</h1>')


class StudentListView(ListView):
    template_name = 'teacher/student.html'
    model = Student

    def get(self, *args, **kwargs):
        if 'mail' not in self.request.session:
            return HttpResponseRedirect('../authorization/')
        if not self.request.session['role'] == 'student':
            return HttpResponseRedirect('../student/')
        return super(StudentListView, self).get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
