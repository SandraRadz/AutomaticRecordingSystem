from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from django.views.generic import ListView

from theme.models import WriteWork


def index(request):
    return render(request, 'themes/themes.html')


class ThemeListView(ListView):
    template_name = 'themes/themes.html'
    model = WriteWork

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
