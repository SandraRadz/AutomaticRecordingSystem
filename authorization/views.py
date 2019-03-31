from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from authorization.authhelper import get_signin_url
from django.urls import reverse


def home(request):
    redirect_uri = request.build_absolute_uri('theme/')
    sign_in_url = get_signin_url(redirect_uri)
    context = {'signin_url': sign_in_url}
    return render(request, 'authorization/authorization.html', context)

    # return HttpResponse('<a href="' + sign_in_url +'">Click here to sign in and view your mail</a>')


def gettoken(request):
    return HttpResponse('gettoken view')
