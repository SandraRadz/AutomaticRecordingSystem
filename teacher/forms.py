from django import forms

from teacher.models import BranchOfKnowledge
from theme.models import WriteWork


class NewTheme(forms.Form):
    work_name = forms.CharField(label='Назва теми', max_length=250)
    english_work_name = forms.CharField(label='English name', required=False, max_length=250)
    note = forms.CharField(label='Примітка', required=False, widget=forms.Textarea)
    branch = forms.ModelMultipleChoiceField(queryset=BranchOfKnowledge.objects.all(), required=False,
                                            to_field_name="branch_name")
    previous_version = forms.ModelChoiceField(queryset=WriteWork.objects.all(), required=False,
                                              to_field_name="work_name")
