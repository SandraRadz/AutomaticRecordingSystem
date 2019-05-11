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
        return super(StudentListView, self).get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(StudentListView, self).get_context_data(**kwargs)
        user_id = self.kwargs.get('user_id')
        context['student'] = Student.objects.get(pk=user_id)
        return context
