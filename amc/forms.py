from django import forms
from django.core import validators
from . import models


class InputAMCScores(forms.ModelForm):
    class Meta:
        model = models.AMCTestResult
        fields = [
            'student', 'test', 'date_tested', 'score',
        ]
