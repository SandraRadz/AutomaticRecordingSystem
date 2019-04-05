from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.db import connection
# Create your views here.
from django.views.generic import ListView
from theme.models import WriteWork
from django.contrib.auth.models import User

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
        return context

    def get_queryset(self, **kwargs):
        """if self.request.GET.get('teacher_name') is not None:
            name = self.request.GET.get('teacher_name')
            cursor = connection.cursor()
            queryset = cursor.execute("SELECT * FROM (theme_writework INNER JOIN teacher_countofhour "
                                      "ON theme_writework.teacher_hour_id = teacher_countofhour.id) "
                                      "INNER JOIN auth_user ON teacher_id = auth_user.id "
                                      "WHERE auth_user.first_name LIKE '%"+name+"%'")
            return queryset"""
        if self.request.GET.get('work_name') is not None:
            queryset = WriteWork.objects.filter(work_name__icontains=self.request.GET.get('work_name'))
            return queryset
        return WriteWork.objects.all()
