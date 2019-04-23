from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import ListView
from django.db.models import Sum
from methodist.models import Methodist
# Create your views here.
from teacher.models import Teacher, StudentGroup, Specialty, TopicOffer, CountOfWork


def index(request):
    if 'mail' not in request.session:
        return HttpResponseRedirect('../authorization/')
    return HttpResponse('<h1>Methodist page</h1>')


class MethodistListView(ListView):
    template_name = 'teacher/methodist.html'
    model = Methodist

    def get(self, *args, **kwargs):

        if 'mail' not in self.request.session:
            return HttpResponseRedirect('../authorization/')
        if not self.request.session['role'] == 'methodist':
            return HttpResponseRedirect('../methodist/')
        return super(MethodistListView, self).get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        methodist = Methodist.objects.get(pk=self.request.session['user_id'])
        context['methodist'] = methodist
        context['teachers'] = Teacher.objects.filter(department=methodist.department)
        spec = Specialty.objects.filter(department__faculty=methodist.department.faculty)
        context['specialties'] = spec
        return context

    def get_queryset(self, **kwargs):
        if self.request.GET.get('teacher') != 'anything' and self.request.GET.get(
                'specialty') != 'anything' and self.request.GET.get(
            'teacher') is not None and self.request.GET.get(
            'amount') is not None and self.request.GET.get('year') is not None and self.request.GET.get(
            'specialty') is not None and self.request.GET.get('yearW') is not None:
            teacher = Teacher.objects.filter(teacher_id=self.request.GET.get('teacher'))
            amount = self.request.GET.get('amount')
            year = self.request.GET.get('year')
            yearW = self.request.GET.get('yearW')
            if teacher:
                if not checkTeacher(self.request.GET.get('teacher'), amount, 2019,  True):
                    teacher = None
            specialty = StudentGroup.objects.filter(year_of_entry=year, specialty__specialty_name=self.request.GET.get(
                'specialty'))
            if not teacher or not specialty:
                return HttpResponseRedirect('../theme')
            res = TopicOffer.objects.get_or_create(count_of_themes=amount, fact_count_of_themes=0, year_of_study=year,
                                                   year_of_work=2019,
                                                   teacher=teacher, specialty=specialty)
        return Methodist.objects.all()


def checkTeacher(teacher_id, amount, year, coursework):
    teacher_amount = TopicOffer.objects.filter(teacher__teacher_id=teacher_id, year_of_work=year).aggregate(Sum('count_of_themes'))['count_of_themes__sum']
    teacher = Teacher.objects.get(pk=teacher_id)
    counts = CountOfWork.objects.get(degree=teacher.degree, academic_status=teacher.academic_status)
    max_amount = 0
    if coursework:
        max_amount = counts.count_of_course_work
    else:
        max_amount = counts.count_of_qualification_work
    return int(amount) + teacher_amount <= max_amount

