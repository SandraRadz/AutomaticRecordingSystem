from django.http import HttpResponseRedirect

# Create your views here.
from django.views.generic import ListView

from student.models import Student


class StudentListView(ListView):
    template_name = 'student/student.html'
    model = Student

    def get(self, *args, **kwargs):
        if 'mail' not in self.request.session:
            return HttpResponseRedirect('../authorization/')
        if not self.request.session['role'] == 'student':
            return HttpResponseRedirect('../student/')
        return super(StudentListView, self).get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(StudentListView, self).get_context_data(**kwargs)
        context['student'] = Student.objects.get(pk=self.request.session['user_id'])
        return context
