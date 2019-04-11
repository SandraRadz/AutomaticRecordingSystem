from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from authorization.authhelper import get_signin_url, get_token_from_code
from authorization.outlookservice import get_me
from student.models import Student
from teacher.models import Teacher
from methodist.models import Methodist

def home(request):
    redirect_uri = request.build_absolute_uri(reverse('authorization:gettoken'))
    sign_in_url = get_signin_url(redirect_uri)
    context = {'signin_url': sign_in_url}
    return render(request, 'authorization/authorization.html', context)


def exit(request):
    if 'mail' not in request.session:
        return HttpResponseRedirect('../authorization/')
    request.session.pop('mail')
    request.session.pop('fullName')
    return HttpResponseRedirect('../authorization/')


def gettoken(request):
    auth_code = request.GET['code']
    redirect_uri = request.build_absolute_uri(reverse('authorization:gettoken'))
    token = get_token_from_code(auth_code, redirect_uri)
    access_token = token['access_token']
    info = get_me(access_token)
    username = info['mail'].split('@')[0]
    if not User.objects.filter(username=username).exists():
        user = User.objects.create_user(username, info['mail'])
        user.first_name = info['displayName']
        user.save()
    user = User.objects.get(username=username)
    request.session['mail'] = info['mail']
    request.session['fullName'] = info['displayName']
    role = None
    if Student.objects.filter(student_id=user.id).exists():
        role = 'student'
    elif Teacher.objects.filter(teacher_id=user.id).exists():
        role = 'teacher'
    elif Methodist.objects.filter(methodist_id=user.id).exists():
        role = 'methodist'
    request.session['role'] = role
    return HttpResponseRedirect('../../theme/')
