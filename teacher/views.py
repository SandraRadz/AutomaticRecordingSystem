from django.http import HttpResponseRedirect
from django.shortcuts import render
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView

from teacher.forms import NewTheme
from teacher.models import Teacher
from theme.models import WriteWork


def index(request):
    if 'mail' not in request.session:
        return HttpResponseRedirect('../authorization/')
    return render(request, 'teacher/teacher.html')


class TeacherListView(ListView):
    template_name = 'teacher/teacher.html'
    model = Teacher

    def get(self, *args, **kwargs):

        if 'mail' not in self.request.session:
            return HttpResponseRedirect('../authorization/')
        if not self.request.session['role'] == 'teacher':
            return HttpResponseRedirect('../teacher/')
        return super(TeacherListView, self).get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['teacher'] = Teacher.objects.get(pk=self.request.session['user_id'])
        context['work_count'] = Teacher.objects.get(pk=self.request.session['user_id'])
        context['themes_list'] = WriteWork.objects.all().filter(teacher_offer__teacher__teacher_id=self.request.session['user_id'])
        return context

@csrf_exempt
def createTheme(request):
    if request.method == 'POST':
        form = NewTheme(request.POST)
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/teacher/')

    else:
        form = NewTheme()

    return render(request, 'teacher/new_theme.html', {'form': form})