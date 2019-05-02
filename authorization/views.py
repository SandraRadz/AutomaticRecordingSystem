import urllib.request

from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from authorization.authhelper import get_signin_url, get_token_from_code
from authorization.outlookservice import get_me
from methodist.models import Methodist
from student.models import Student
from teacher.models import Teacher, BranchOfKnowledge


def home(request):
    if 'mail' in request.session:
        return HttpResponseRedirect('../')
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
    mail = None
    if info['mail']:
        mail = info['mail']
    else:
        mail = info['userPrincipalName']
    username = mail.split('@')[0]
    if not User.objects.filter(username=username).exists():
        user = User.objects.create_user(username, mail)
        user.first_name = info['displayName']
        user.save()
    user = User.objects.get(username=username)
    request.session['mail'] = mail  # info['mail']
    request.session['fullName'] = info['displayName']
    role = None
    if Student.objects.filter(student_id=user.id).exists():
        role = 'student'
    elif Teacher.objects.filter(teacher_id=user.id).exists():
        role = 'teacher'
    elif Methodist.objects.filter(methodist_id=user.id).exists():
        role = 'methodist'
    request.session['role'] = role
    request.session['user_id'] = user.id
    if role == 'teacher':
        find_branches(user.id)
    return HttpResponseRedirect('../../')


def find_branches(idk):
    quote_page = Teacher.objects.get(pk=idk).google_scholar
    if not quote_page:
        return
    page = urllib.request.urlopen(quote_page)
    soup = BeautifulSoup(page, 'html.parser')
    name_box = soup.findAll('a', attrs={'class': 'gsc_prf_inta gs_ibl'})
    teacher = Teacher.objects.get(pk=idk)
    for n in name_box:
        br = BranchOfKnowledge.objects.get_or_create(branch_name=n.text.strip())
        teacher.branch.add(br[0])
    teacher.save()
    return
