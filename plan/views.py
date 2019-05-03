from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView

# Create your views here.
from plan.models import Plan
from student.models import Student
from teacher.models import StudentGroup, Department, Protection
from theme.models import Record, WriteWork


def index(request):
    if 'mail' not in request.session:
        return HttpResponseRedirect('../authorization/')
    return render(request, 'plans/plans.html')


class PlanListView(ListView):
    template_name = 'plans/plans.html'
    model = Plan

    def get(self, *args, **kwargs):
        if 'mail' not in self.request.session:
            return HttpResponseRedirect('../authorization/')
        return super(PlanListView, self).get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PlanListView, self).get_context_data(**kwargs)
        user_id = self.request.session['user_id']
        if self.request.session['role'] == 'student':
            user_record = Record.objects.all().filter(student=user_id, status='CONFIRMED')
            if user_record:
                user_record = user_record[0]
            else:
                return context
            work = WriteWork.objects.get(pk=user_record.work_id)
            context['work'] = work
            plan_list = Plan.objects.all().filter(work_name_id=work.id)
            context['plan'] = plan_list
            student = Student.objects.get(pk=user_id)
            group = student.specialty
            department = work.teacher_offer.teacher.department
            prot = Protection\
                .objects.all().filter(speciality_group=group, teacher_department=department)
            if prot:
                protection = prot[0]
            else:
                protection = None
            context['protection'] = protection
        return context
