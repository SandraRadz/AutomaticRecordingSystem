import datetime

from django import forms


class NewPlanItem(forms.Form):
    deadline = forms.DateField(initial=datetime.date.today)
    description = forms.CharField(label='Опис', required=False, widget=forms.Textarea)
