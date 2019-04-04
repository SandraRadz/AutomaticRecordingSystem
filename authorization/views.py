from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from authorization.authhelper import get_signin_url, get_token_from_code
from authorization.outlookservice import get_me


def home(request):
    redirect_uri = request.build_absolute_uri(reverse('authorization:gettoken'))
    sign_in_url = get_signin_url(redirect_uri)
    context = {'signin_url': sign_in_url}
    return render(request, 'authorization/authorization.html', context)

def gettoken(request):
    auth_code = request.GET['code']
    redirect_uri = request.build_absolute_uri(reverse('authorization:gettoken'))
    token = get_token_from_code(auth_code, redirect_uri)
    access_token = token['access_token']
    info = get_me(access_token)
    request.session['mail'] = info['mail']
    username = info['mail'].split('@')[0]
    if not User.objects.filter(username=username).exists():
        user = User.objects.create_user(username, info['mail'])
        user.first_name = info['displayName'].split(' ')[1]
        user.last_name = info['displayName'].split(' ')[0]
        user.save()
    return HttpResponseRedirect('../theme/')