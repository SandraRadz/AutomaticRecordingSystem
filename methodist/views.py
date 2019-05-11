import calendar

from django.db.models import Sum
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import ListView
import datetime
from django.db.models import Q

from methodist.models import Methodist
# Create your views here.
from teacher.models import Teacher, StudentGroup, Specialty, TopicOffer, CountOfWork


class MethodistListView(ListView):
    template_name = 'methodist/methodist.html'
    model = Methodist

    def get(self, *args, **kwargs):

        if 'mail' not in self.request.session:
            return HttpResponseRedirect('../authorization/')
        if self.request.session['role'] != 'methodist' or str(self.request.session['user_id']) != str(self.kwargs.get('user_id')):
            return HttpResponseRedirect('/'+self.request.session['role']+'/'+str(self.request.session['user_id']))
        return super(MethodistListView, self).get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        methodist = Methodist.objects.get(pk=self.request.session['user_id'])
        methodist_department = methodist.department
        context['methodist'] = methodist
        context['years'] = [1, 2, 3, 4, 5, 6]
        context['teachers'] = Teacher.objects.filter(department=methodist.department)
        spec = Specialty.objects.filter(department__faculty=methodist.department.faculty)
        context['specialties'] = spec
        context['topics_offers'] = TopicOffer.objects.all().filter(teacher__department=methodist_department).order_by(
            'specialty__specialty__specialty_name').order_by('teacher__teacher_id__first_name')
        return context

    def get_queryset(self, **kwargs):
        if self.request.GET.get('del_offer') is not None:
            offer_id = self.request.GET.get('del_offer')
            offer = TopicOffer.objects.get(pk=offer_id)
            offer.delete()

        elif self.request.GET.get('teacher') != 'anything' and \
                self.request.GET.get('specialty') != 'anything' and \
                self.request.GET.get('year') != 'anything' and \
                self.request.GET.get('teacher') is not None and \
                self.request.GET.get('amount') is not None and \
                self.request.GET.get('year') is not None and \
                self.request.GET.get('specialty') is not None:
            teacher = Teacher.objects.get(pk=self.request.GET.get('teacher'))
            amount = self.request.GET.get('amount')
            year = int(self.request.GET.get('year'))
            specialty = self.request.GET.get('specialty')
            if year > 4:
                degree = 'master'
                year_of_entry = datetime.datetime.now().year - year + 4
                if datetime.datetime.now().month > 9:
                    year_of_entry = year_of_entry + 1
            else:
                degree = 'bachelor'
                year_of_entry = datetime.datetime.now().year - year
                if datetime.datetime.now().month > 9:
                    year_of_entry = year_of_entry + 1

            specialty_obj = StudentGroup.objects.filter(year_of_entry=year_of_entry,
                                                        specialty__specialty_name=specialty, degree=degree)[0]
            if not checkAmount(teacher, amount, year):
                print("too much themes")
                return HttpResponseRedirect('../theme')
            if not specialty:
                print("Specialty")
                return HttpResponseRedirect('../theme')
            TopicOffer.objects.create(count_of_themes=amount, fact_count_of_themes=0, year_of_study=year,
                                      teacher=teacher,
                                      specialty=specialty_obj)
        return Methodist.objects.all()


def checkAmount(teacher, amount, year):
    counts = CountOfWork.objects.get(degree=teacher.degree, academic_status=teacher.academic_status)
    if counts:
        cource_norm = counts.count_of_course_work
        qualif_norm = counts.count_of_qualification_work
    else:
        cource_norm = 8
        qualif_norm = 8
    cource_fact = TopicOffer.objects.filter(Q(teacher=teacher, year_of_study=1) | Q(teacher=teacher, year_of_study=2) |
                                            Q(teacher=teacher, year_of_study=3) |
                                            Q(teacher=teacher, year_of_study=5)).aggregate(Sum('count_of_themes'))[
        'count_of_themes__sum']
    qualif_fact = TopicOffer.objects.filter(Q(teacher=teacher, year_of_study=4) |
                                            Q(teacher=teacher, year_of_study=6)).aggregate(Sum('count_of_themes'))[
        'count_of_themes__sum']
    if not cource_fact:
        cource_fact = 0
    if not qualif_fact:
        qualif_fact = 0
    if year == 4 or year == 6:
        return qualif_norm >= qualif_fact + int(amount)
    return cource_norm >= cource_fact + int(amount)


