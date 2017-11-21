from django import forms
from brain.models import StudentRoster
from .models import CGI, CGIResult


class CGIResultsForm(forms.ModelForm):
    class Meta:
        model = CGIResult
        fields = [
            'student', 'cgi', 'progress'
        ]
        widgets = {
            'progress': forms.RadioSelect,
        }


class CGIForm(forms.Form):
    answer = forms.IntegerField()
    # Need to send through the numbers that the student worked with, as they are random. have to lock them in so we can
    # Check the answer and see if it's correct.
