from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import ListView

# Create your views here.
from teacher.models import Teacher
from theme.models import WriteWork, Record


def index(request):
    if 'mail' not in request.session:
        return HttpResponseRedirect('../authorization/')
    return HttpResponse('<h1>Information page</h1>')


class InfoListView(ListView):
    template_name = 'info/info.html'
    model = Teacher

    def get(self, *args, **kwargs):
        if 'mail' not in self.request.session:
            return HttpResponseRedirect('../authorization/')
        return super(InfoListView, self).get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(InfoListView, self).get_context_data(**kwargs)

        works = Record.objects.filter(status='CONFIRMED')
        years = works.values_list('work__year_of_work', flat=True).distinct()
        stats = {}
        for y in years:
            arr = []
            for w in works:
                if w.work.year_of_work == y:
                    arr.append(w)
            stats[y] = arr
        context['stats'] = stats
        return context
