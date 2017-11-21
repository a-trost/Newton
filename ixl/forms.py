from django import forms
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


class ListSettings(forms.Form):
    bonus_challenges = forms.IntegerField(initial=15)
    use_diagnostic_for_bonus = forms.BooleanField(help_text="If you want to use IXL's diagnostic suggestions. They will be added as part of the bonus challenges.", initial=True)
