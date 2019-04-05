from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
from django.views.generic import ListView

from theme.models import WriteWork


class ThemeListView(ListView):
    template_name = 'themes/themes_teacher.html'
    model = WriteWork

    def get(self, *args, **kwargs):
        if 'mail' not in self.request.session:
            return HttpResponseRedirect('../authorization/')
        return super(ThemeListView, self).get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

