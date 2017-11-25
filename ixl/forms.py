from django import forms
from django.core.validators import RegexValidator

from .models import IXLListAssignment, IXLList


# class IXLListForm(forms.ModelForm):
#     class Meta:
#         model = IXLList
#         fields = [
#             'title', 'author', 'category',
#         ]

class CreateIXLListForm(forms.Form):
    title = forms.CharField()
    category = forms.ChoiceField(choices=(("Unit", "Unit"), ("Remediation", "Remediation"), ("Enrichment", "Enrichment"), ("Test", "Test"), ("Other", "Other")))


class CreateIXLListExerciseForm(forms.Form):
    ixl_format = RegexValidator(r'^\w+\.\d+$', 'Pattern must match IXL format: A.12')
    grade = forms.CharField(max_length=1, widget=forms.TextInput(attrs={'size': '2'}))
    id_code = forms.CharField(validators=[ixl_format], max_length=5)
    required_score = forms.CharField(label="Required Score")

class ListSettings(forms.Form):
    bonus_challenges = forms.IntegerField(initial=15)
    use_diagnostic_for_bonus = forms.BooleanField(help_text="If you want to use IXL's diagnostic suggestions. They will be added as part of the bonus challenges.", initial=True)
