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
        context['user_profile'] = (str(user_id) == str(self.request.session['user_id']))
        context['student'] = Student.objects.get(pk=user_id)
        return context

    def get_queryset(self, **kwargs):
        student_id = self.request.GET.get('student_id')
        avr_mark = self.request.GET.get('avr_mark')
        s_email = self.request.GET.get('s_email')
        if student_id:
            student_for_edit = Student.objects.get(pk=student_id)
            if avr_mark == "":
                avr_mark = 0
            if float(avr_mark) > 100 or float(avr_mark) < 0:
                avr_mark = 0
            student_for_edit.average_mark = avr_mark
            student_for_edit.additional_email = s_email
            student_for_edit.save()

        return Student.objects.all()
