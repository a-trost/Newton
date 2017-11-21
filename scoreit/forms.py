from django import forms
from django.core import validators
from . import models


class ScoreForm(forms.ModelForm):
    class Meta:
        model = models.Score
        fields = ['hand', 'slant', 'transition', 'please', 'instruction', 'material', 'peer']
        widgets = {
            'hand': forms.RadioSelect,
            'slant': forms.RadioSelect,
            'transition': forms.RadioSelect,
            'please': forms.RadioSelect,
            'instruction': forms.RadioSelect,
            'material': forms.RadioSelect,
            'peer': forms.RadioSelect,
        }

