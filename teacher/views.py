from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView

from teacher.forms import NewTheme
from teacher.models import Teacher, TopicOffer, BranchOfKnowledge
from theme.models import WriteWork, Record


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
        context['themes_list'] = WriteWork.objects.all().filter(
            teacher_offer__teacher__teacher_id=self.request.session['user_id'])
        context['teacher_offer'] = TopicOffer.objects.all().filter(teacher__teacher_id=self.request.session['user_id'])
        all_records = Record.objects.all()
        context['all_records'] = all_records
        return context

    def get_queryset(self, **kwargs):
        if self.request.GET.get('del_theme') is not None:
            theme_id = self.request.GET.get('del_theme')

            theme = WriteWork.objects.get(pk=theme_id)

            theme.delete()
        return Teacher.objects.all()


@csrf_exempt
def createTheme(request):
    if request.method == 'POST':
        form = NewTheme(request.POST)
        if form.is_valid():
            teacher = Teacher.objects.get(pk=request.session['user_id'])
            offer = TopicOffer.objects.all().filter(teacher=teacher)[0]
            work_name = request.POST.get('work_name', '')
            english_work_name = request.POST.get('english_work_name', '')
            note = request.POST.get('note', '')
            previous_version = form.cleaned_data.get('previous_version', '')
            branch = form.cleaned_data.get('branch', '')
            feedback_obj = WriteWork.objects.create(work_name=work_name, english_work_name=english_work_name, note=note, teacher_offer=offer, previous_version=previous_version)
            feedback_obj.branch.set(branch)

            return HttpResponseRedirect('/teacher/')
    else:
        form = NewTheme()
    return render(request, 'teacher/new_theme.html', {'form': form})
