import smtplib
import ssl

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
        context['branches'] = BranchOfKnowledge.objects.all()
        context['statuses'] = dict(Record.STATUS_TITLE).values()
        if self.request.session['role'] == 'student':
            faculty = Student.objects.filter(student_id=self.request.session['user_id'])[
                0].specialty.specialty.department.faculty
            context['departments'] = Department.objects.filter(faculty=faculty)
            student = Student.objects.get(pk=self.request.session['user_id'])
            records = Record.objects.filter(student_id=student).values_list('work', flat=True)
            context['records'] = records
            booked_records = Record.objects.filter(status='CONFIRMED').values_list('work', flat=True)
            context['booked_records'] = booked_records
            this_stud_rec = Record.objects.filter(student_id=student)
            context['is_confirmed'] = False
            for record in this_stud_rec:
                if record.status == 'CONFIRMED':
                    context['is_confirmed'] = True
                    context['user_work'] = record.work_id
        elif self.request.session['role'] == 'teacher':
            faculty = Teacher.objects.filter(teacher_id=self.request.session['user_id'])[0].department.faculty
            context['departments'] = Department.objects.filter(faculty=faculty)
        else:
            context['departments'] = Department.objects.all()
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
            #send_email_cancel(student, theme)

        if self.request.GET.get('theme_id') is not None:
            student = Student.objects.get(pk=self.request.session['user_id'])
            theme_id = self.request.GET.get('theme_id')
            theme = WriteWork.objects.get(pk=theme_id)
            Record.objects.get_or_create(student=student, work=theme)
            #send_email_record(student, theme)

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


def send_email_record(student, theme):
    port = 465
    smtp_server = "smtp.gmail.com"
    sender_email = "naukma.recording@gmail.com"
    receiver_email = User.objects.get(pk=theme.teacher_offer.teacher_id).email
    password = 'naukma912'
    message = 'На Вашу тему "' + theme.work_name + '" записався студент ' + User.objects.get(pk=student.pk).first_name
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.encode('utf-8', 'ignore'))
        server.quit()


def send_email_cancel(student, theme):
    port = 465
    smtp_server = "smtp.gmail.com"
    sender_email = "naukma.recording@gmail.com"
    receiver_email = User.objects.get(pk=theme.teacher_offer.teacher_id).email
    password = 'naukma912'
    message = 'З Вашої теми "' + theme.work_name + '" виписався студент ' + User.objects.get(
        pk=student.pk).first_name
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.encode('utf-8', 'ignore'))
        server.quit()
