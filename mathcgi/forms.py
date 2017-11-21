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




