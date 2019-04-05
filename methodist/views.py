from django.http import HttpResponseRedirect, HttpResponse
from teacher.models import Methodist
from django.views.generic import ListView


# Create your views here.

def index(request):
    if 'mail' not in request.session:
        return HttpResponseRedirect('../authorization/')
    return HttpResponse('<h1>Methodist page</h1>')


class MethodistListView(ListView):
    template_name = 'teacher/methodist.html'
    model = Methodist

    def get(self, *args, **kwargs):

        if 'mail' not in self.request.session:
            return HttpResponseRedirect('../authorization/')
        if not self.request.session['role'] == 'methodist':
            return HttpResponseRedirect('../methodist/')
        return super(MethodistListView, self).get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
