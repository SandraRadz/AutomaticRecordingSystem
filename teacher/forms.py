from django import forms


class NewTheme(forms.Form):
    work_name = forms.CharField(label='Назва теми', max_length=500)
    english_work_name = forms.CharField(label='English name ', max_length=500)
    note = forms.CharField()
    # previous_version = forms.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    # branch = forms.ManyToManyField(BranchOfKnowledge)