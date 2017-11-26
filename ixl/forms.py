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
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 3, 'cols': 15}))


class IXLListExerciseForm(forms.Form):
    ixl_format = RegexValidator(r'^\w+\.\d+$', 'Pattern must match IXL format: A.12')
    grade = forms.CharField(max_length=1, widget=forms.TextInput(attrs={'size': '2'}))
    id_code = forms.CharField(validators=[ixl_format], max_length=5)
    required_score = forms.CharField(label="Required Score", initial=80)


from django.forms.formsets import BaseFormSet


class BaseIXLListExerciseFormSet(BaseFormSet):
    def clean(self):
        """
        Adds validation to check that the same exercise does not appear twice
        """
        if any(self.errors):
            return
        # This will hold Tuples with grade, id_code, required_score:
        grade_id_scores = []
        duplicates = False

        for form in self.forms:
            if form.cleaned_data:
                grade = form.cleaned_data['grade']
                id_code = form.cleaned_data['id_code']
                required_score = form.cleaned_data['required_score']
                if not required_score:
                    required_score = 80
                if not grade:
                    raise forms.ValidationError("You need to enter a grade!")
                if grade and id_code and required_score:
                    if (grade, id_code, required_score) in grade_id_scores:
                        duplicates = True
                        grade_id_scores.append((grade, id_code, required_score))

                if duplicates:
                    raise forms.ValidationError(
                        'Exercises must be unique. You can only have the same exercise in twice if they have different Required Scores.',
                        code='duplicate_links'
                    )

                    # Check that all links have both an anchor and URL
                    # if url and not anchor:
                    #     raise forms.ValidationError(
                    #         'All links must have an anchor.',
                    #         code='missing_anchor'
                    #     )
                    # elif anchor and not url:
                    #     raise forms.ValidationError(
                    #         'All links must have a URL.',
                    #         code='missing_URL'
                    #     )



class ListSettings(forms.Form):
    bonus_challenges = forms.IntegerField(initial=15)
    use_diagnostic_for_bonus = forms.BooleanField(help_text="If you want to use IXL's diagnostic suggestions. They will be added as part of the bonus challenges.", initial=True)


class IXLListAssignmentModelForm(forms.ModelForm):
    class Meta:
        model = IXLListAssignment
        fields = ['student', 'ixl_list', 'assigned', 'number_to_assign', 'date_created']
