from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
import smtplib
import ssl
from student.models import Student
from teacher.forms import NewTheme
from teacher.models import Teacher, TopicOffer, StudentGroup
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
        user_id = self.request.session['user_id']
        context['teacher'] = Teacher.objects.get(pk=user_id)
        context['work_count'] = Teacher.objects.get(pk=user_id)
        context['themes_list'] = WriteWork.objects.all().filter(
            teacher_offer__teacher__teacher_id=user_id)
        context['teacher_offer_bach'] = TopicOffer.objects.filter(
            specialty__in=StudentGroup.objects.filter(degree='bachelor'),
            teacher__teacher_id=user_id)
        context['teacher_offer_mag'] = TopicOffer.objects.filter(
            specialty__in=StudentGroup.objects.filter(degree='master'),
            teacher__teacher_id=user_id)
        all_records = Record.objects.all()
        context['all_records'] = all_records
        return context

    def get_queryset(self, **kwargs):
        if self.request.GET.get('del_theme') is not None:
            theme_id = self.request.GET.get('del_theme')
            theme = WriteWork.objects.get(pk=theme_id)
            offer = theme.teacher_offer
            offer.fact_count_of_themes = offer.fact_count_of_themes-1
            offer.save()
            theme.delete()
        elif self.request.GET.get('choose_student') is not None:
            record_id = self.request.GET.get('choose_student')
            record = Record.objects.get(pk=record_id)
            work = record.work_id
            student = record.student_id
            record.status = 'CONFIRMED'
            record.save()
            send_email(student, work)

            other_record_on_theme = Record.objects.all().filter(work_id=work)
            for o_rec in other_record_on_theme:
                if o_rec != record:
                    if o_rec.status != 'BLOCKED':
                        o_rec.status = 'REJECTED'
                        o_rec.save()

            other_record_of_student = Record.objects.all().filter(student_id=student)
            for o_stud in other_record_of_student:
                if o_stud != record:
                    o_stud.status = 'BLOCKED'
                    o_stud.save()

        elif self.request.GET.get('cancel_student') is not None:
            record_id = self.request.GET.get('cancel_student')
            record = Record.objects.get(pk=record_id)
            work = record.work_id
            student = record.student_id
            record.status = 'WAIT'
            record.save()

            other_record_on_theme = Record.objects.all().filter(work_id=work)
            for o_rec in other_record_on_theme:
                if o_rec.status == 'REJECTED' or o_rec.status == 'CONFIRMED':
                    o_rec.status = 'WAIT'
                    o_rec.save()

            other_record_of_student = Record.objects.all().filter(student_id=student)
            for o_stud in other_record_of_student:
                if o_stud.status == 'BLOCKED':
                    o_stud.status = 'WAIT'
                    o_stud.save()

        return Teacher.objects.all()


@csrf_exempt
def createTheme(request):
    if request.method == 'POST':
        form = NewTheme(request.POST)

        if form.is_valid():
            teacher = Teacher.objects.get(pk=request.session['user_id'])
            specialty = form.cleaned_data.get('specialty', '')
            offer = TopicOffer.objects.all().filter(teacher=teacher,
                                                    specialty__specialty__specialty_name=specialty.specialty
                                                    .specialty.specialty_name,
                                                    specialty__year_of_entry=specialty.specialty.year_of_entry)
            if offer:
                offer = offer[0]
            else:
                return render(request, 'teacher/new_theme.html', {'form': form})
            if offer and offer.fact_count_of_themes < offer.count_of_themes:
                offer.fact_count_of_themes += 1
                offer.save()
                work_name = request.POST.get('work_name', '')
                english_work_name = request.POST.get('english_work_name', '')
                note = request.POST.get('note', '')
                previous_version = form.cleaned_data.get('previous_version', '')
                branch = form.cleaned_data.get('branch', '')
                write_work_obj = WriteWork.objects.create(work_name=work_name, english_work_name=english_work_name,
                                                        note=note, teacher_offer=offer,
                                                        previous_version=previous_version)
                write_work_obj.branch.set(branch)
                return HttpResponseRedirect('/teacher/')
    else:
        form = NewTheme()
    return render(request, 'teacher/new_theme.html', {'form': form})


def send_email(st, w):
    work = WriteWork.objects.filter(pk=w)[0]
    port = 465
    smtp_server = "smtp.gmail.com"
    sender_email = "naukma.recording@gmail.com"
    receiver_email = User.objects.get(pk=st).email
    password = 'naukma912'
    message = 'Вітаємо! Вас було затверджено на тему "' + work.work_name + '".'
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.encode('utf-8', 'ignore'))
        server.quit()
    return
