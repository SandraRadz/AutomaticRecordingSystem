from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
import smtplib
import ssl
import datetime
from student.models import Student
from teacher.forms import NewTheme
from teacher.models import Teacher, TopicOffer, StudentGroup, BranchOfKnowledge
from theme.models import WriteWork, Record


class TeacherListView(ListView):
    template_name = 'teacher/teacher.html'
    model = Teacher

    def get(self, *args, **kwargs):
        if 'mail' not in self.request.session:
            return HttpResponseRedirect('../authorization/')
        return super(TeacherListView, self).get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs.get('user_id')
        context['user_profile'] = (int(user_id) == int(self.request.session['user_id']))
        teacher = Teacher.objects.get(pk=user_id)
        context['teacher'] = teacher
        context['branches'] = BranchOfKnowledge.objects.filter(teacher=teacher)
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
            offer.fact_count_of_themes = offer.fact_count_of_themes - 1
            offer.save()
            theme.delete()
        elif self.request.GET.get('choose_student') is not None:
            record_id = self.request.GET.get('choose_student')
            choose_student(record_id)

        elif self.request.GET.get('cancel_student') is not None:
            record_id = self.request.GET.get('cancel_student')
            cancel_stud(record_id)

        work_id = self.request.GET.get('work_id')
        work_name = self.request.GET.get('work_name')
        en_name = self.request.GET.get('english_work_name')
        note = self.request.GET.get('note')
        if work_id and work_name:
            theme_for_edit = WriteWork.objects.get(pk=work_id)
            theme_for_edit.work_name = work_name
            theme_for_edit.english_work_name = en_name
            theme_for_edit.note = note
            theme_for_edit.save()

        teacher_edit_id = self.request.GET.get('teacher_edit_id')
        s_email = self.request.GET.get('s_email')
        phone = self.request.GET.get('phone')
        office = self.request.GET.get('office')
        if teacher_edit_id:
            teacher_for_edit = Teacher.objects.get(pk=teacher_edit_id)
            teacher_for_edit.additional_email = s_email
            teacher_for_edit.phone = phone
            teacher_for_edit.office = office
            teacher_for_edit.save()

        return Teacher.objects.all()


def choose_student(record_id):
    record = Record.objects.get(pk=record_id)
    work = record.work_id

    before_conf_student = Record.objects.all().filter(work_id=work, status='CONFIRMED')
    if before_conf_student:
        cancel_stud(before_conf_student[0].id)

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


def cancel_stud(record_id):
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


@csrf_exempt
def createTheme(request, spec):
    request.session['spec'] = spec
    if request.method == 'POST':
        form = NewTheme(request.POST)
        user_id = request.session['user_id']
        if form.is_valid():
            teacher = Teacher.objects.get(pk=user_id)
            sp_year = datetime.datetime.now().year - int(str(spec).split('-')[1])
            sp_name = str(spec).split('-')[0]
            specialty = StudentGroup.objects.all().filter(specialty__specialty_name=sp_name, year_of_entry=sp_year)[0]
            offer = TopicOffer.objects.all().filter(teacher=teacher,
                                                    specialty__specialty__specialty_name=sp_name,
                                                    specialty__year_of_entry=sp_year)
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
                return HttpResponseRedirect('/teacher/' + str(user_id))
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
    try:
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.encode('utf-8', 'ignore'))
            server.quit()
    except smtplib.SMTPRecipientsRefused as e:
        print(e)
    return
