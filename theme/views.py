from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.views.generic import ListView

from student.models import Student
from teacher.models import Teacher, TopicOffer, Department, BranchOfKnowledge
from theme.models import WriteWork, Record


class ThemeListView(ListView):
    template_name = 'themes/themes.html'
    model = WriteWork

    def get(self, *args, **kwargs):
        self.object_list = self.get_queryset()
        if 'mail' not in self.request.session:
            return HttpResponseRedirect('../authorization/')
        return super(ThemeListView, self).get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = User
        all_records = Record.objects.all()
        context['all_records'] = all_records
        context['cathedras'] = Department.objects.all()
        context['branches'] = BranchOfKnowledge.objects.all()
        context['statuses'] = dict(Record.STATUS_TITLE).values()
        if self.request.session['role'] == 'student':
            student = Student.objects.get(pk=self.request.session['user_id'])
            records = Record.objects.filter(student_id=student).values_list('work', flat=True)
            context['records'] = records
        return context

    def get_queryset(self, **kwargs):
        if self.request.GET.get('department') is not None or self.request.GET.get(
                'branch') is not None or self.request.GET.get('status') is not None:
            department = self.request.GET.get('department')
            branch = self.request.GET.get('branch')
            status = self.request.GET.get('status')
            queryset = []
            empty = True
            if department != 'anything':
                dep = Department.objects.get(department_name=department)
                queryset = WriteWork.objects.filter(teacher_offer__teacher__department=dep)
                empty = False
            if branch != 'anything':
                br = BranchOfKnowledge.objects.get(branch_name=branch)
                query = WriteWork.objects.filter(branch__branch_name=br)
                queryset = list(set(query) & set(queryset)) if queryset else query
                empty = False
            if status != 'anything':
                sts = dict(Record.STATUS_TITLE)
                st = [key for key, value in sts.items() if value == status][0]
                query = WriteWork.objects.filter(pk__in=Record.objects.filter(status=st).values_list('work', flat=True))
                queryset = list(set(query) & set(queryset)) if queryset else query
                empty = False
            if not empty:
                return queryset
        if self.request.GET.get('theme') is not None:
            student = Student.objects.get(pk=self.request.session['user_id'])
            theme_id = self.request.GET.get('theme')
            theme = WriteWork.objects.get(pk=theme_id)
            Record.objects.filter(student=student, work=theme).delete()
        if self.request.GET.get('theme_id') is not None:
            student = Student.objects.get(pk=self.request.session['user_id'])
            theme_id = self.request.GET.get('theme_id')
            theme = WriteWork.objects.get(pk=theme_id)
            record = Record.objects.get_or_create(student=student, work=theme, status="WAIT")

        if self.request.GET.get('teacher_name') is not None:
            users = User.objects.filter(first_name__icontains=self.request.GET.get('teacher_name')) \
                .values_list('id', flat=True)
            teachers = Teacher.objects.filter(teacher_id__in=users).values_list('teacher_id', flat=True)
            places = TopicOffer.objects.filter(teacher__in=teachers).values_list('id', flat=True)
            queryset = WriteWork.objects.filter(teacher_offer__in=places)
            return queryset
        if self.request.GET.get('work_name') is not None:
            queryset = WriteWork.objects.filter(work_name__icontains=self.request.GET.get('work_name'))
            return queryset
        return WriteWork.objects.all()
