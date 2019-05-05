from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView

# Create your views here.
from methodist.models import Methodist
from plan.forms import NewPlanItem
from plan.models import Plan
from student.models import Student
from teacher.models import StudentGroup, Department, Protection, Teacher
from theme.models import Record, WriteWork


def index(request):
    if 'mail' not in request.session:
        return HttpResponseRedirect('../authorization/')
    return render(request, 'plans/plans.html')


class PlanListView(ListView):
    template_name = 'plans/plan_helper.html'
    model = Plan

    def get(self, *args, **kwargs):
        if 'mail' not in self.request.session:
            return HttpResponseRedirect('../authorization/')
        if self.request.session['role'] == 'student':
            user_id = self.request.session['user_id']
            user_record = Record.objects.all().filter(student=user_id, status='CONFIRMED')
            if user_record:
                user_record = user_record[0]
                work = user_record.work_id
                return HttpResponseRedirect('/plan/' + str(work))
        return super(PlanListView, self).get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PlanListView, self).get_context_data(**kwargs)
        user_id = self.request.session['user_id']
        if self.request.session['role'] == 'teacher':
            teacher = Teacher.objects.get(pk=user_id)
            context['work_titles'] = WriteWork.objects.filter(teacher_offer__teacher=teacher)
            context['plan_items'] = Plan.objects.filter(work_name__teacher_offer__teacher_id=user_id)

        elif self.request.session['role'] == 'methodist':
            methodist = Methodist.objects.get(pk=user_id)
            department = Department.objects.get(pk=methodist.department.id)
            protection = Protection.objects.filter(teacher_department=department)
            context['protection'] = protection
            groups = StudentGroup.objects.filter(specialty__department=department)

        return context


class PlanItemListView(ListView):
    template_name = 'plans/plans.html'
    model = Plan

    def get(self, *args, **kwargs):
        if 'mail' not in self.request.session:
            return HttpResponseRedirect('../authorization/')
        if self.request.session['role'] == 'student':
            user_id = self.request.session['user_id']
            user_record = Record.objects.all().filter(student=user_id, status='CONFIRMED')
            if user_record:
                user_record = user_record[0]
                work = user_record.work_id
                print(work)
                print(self.kwargs.get('plan_url'))
                if str(work) != self.kwargs.get('plan_url'):
                    return HttpResponseRedirect('/plan/' + str(work))
        if self.request.GET.get('del_item') is not None:
            del_item = self.request.GET.get('del_item')
            plan_item = Plan.objects.get(pk=del_item)
            plan_item.delete()
        return super(PlanItemListView, self).get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PlanItemListView, self).get_context_data(**kwargs)
        work_url = self.kwargs.get('plan_url')
        work = WriteWork.objects.get(pk=work_url)
        context['work'] = work
        plan_list = Plan.objects.all().filter(work_name_id=work.id).order_by('deadline')
        context['plan'] = plan_list
        student_record = Record.objects.filter(work_id=work_url, status='CONFIRMED')
        if student_record:
            context['student_record'] = student_record[0].student.student_id.first_name
        else:
            context['student_record'] = None
        group = work.teacher_offer.specialty
        department = work.teacher_offer.teacher.department
        prot = Protection.objects.all().filter(speciality_group=group, teacher_department=department)
        if prot:
            protection = prot[0]
        else:
            protection = None
        context['protection'] = protection
        return context


@csrf_exempt
def addPlanItem(request, plan_url):
    if request.method == 'POST':
        form = NewPlanItem(request.POST)
        if form.is_valid():
            work = WriteWork.objects.get(pk=plan_url)
            deadline=request.POST.get('deadline', '')
            description=request.POST.get('description', '')
            plan_item=Plan.objects.create(work_name=work, deadline=deadline, description=description)
            plan_item.save()
            return HttpResponseRedirect('/plan/'+str(plan_url))
    else:
        form = NewPlanItem()
    return render(request, 'plans/new_plan_item.html', {'form': form})

