from django import forms
from django.forms import TextInput
from django.core import validators
from . import models


class InputNWEAScores(forms.ModelForm):
    class Meta:
        model = models.NWEAScore
        fields = [
            "student",
            "season",
            "subdomain1",
            "subdomain2",
            "subdomain3",
            "subdomain4",
            "subdomain5",
            "subdomain6",
            "subdomain7",
            "subdomain8",
        ]
        widgets = {'subdomain1': TextInput(), "subdomain2":TextInput(), "subdomain3":TextInput(),"subdomain4":TextInput(),
                   "subdomain5": TextInput(),"subdomain6":TextInput(),"subdomain7":TextInput(),"subdomain8":TextInput(),}