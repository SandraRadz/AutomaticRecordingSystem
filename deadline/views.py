from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView

from methodist.models import Methodist
from teacher.models import Protection, Department, StudentGroup, Faculty


class DeadlineListView(ListView):
    template_name = 'deadline/deadline.html'

    def get(self, *args, **kwargs):
        if 'mail' not in self.request.session:
            return HttpResponseRedirect('../authorization/')
        if self.request.session['role'] != 'methodist':
            return HttpResponseRedirect('/plan/')
        return super(DeadlineListView, self).get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        # should I check one more time if user is methodist?
        context = super(DeadlineListView, self).get_context_data(**kwargs)
        user_id = self.request.session['user_id']
        methodist = Methodist.objects.get(pk=user_id)
        department = Department.objects.get(pk=methodist.department.id)
        faculty = Faculty.objects.get(pk=methodist.department.faculty.id)
        protection = Protection.objects.filter(teacher_department=department)
        context['protection'] = protection
        groups = StudentGroup.objects.filter(specialty__department__faculty=faculty)
        context['groups'] = groups
        return context

    def get_queryset(self, **kwargs):
        if self.request.GET.get('del_date') is not None:
            del_id = self.request.GET.get('del_date')
            date_item = Protection.objects.get(pk=del_id)
            date_item.delete()
        user_id = self.request.session['user_id']
        methodist = Methodist.objects.get(pk=user_id)
        department = Department.objects.get(pk=methodist.department.id)
        group_id = self.request.GET.get('group')
        pre_protection = self.request.GET.get('pre-protection')
        protection = self.request.GET.get('protection')
        if group_id != 'anything' and pre_protection and protection:
            group = StudentGroup.objects.get(pk=int(group_id))
            if Protection.objects.filter(speciality_group=group).count() == 0:
                Protection.objects.create(speciality_group=group, teacher_department=department,
                                          date_of_pre_protection=pre_protection,
                                          date_of_confirmation=protection)

        return Methodist.objects.all()
