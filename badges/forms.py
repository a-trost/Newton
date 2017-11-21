from brain.models import StudentRoster
from badges.models import Avatar

from django import forms

class AvatarForm(forms.ModelForm):
    class Meta:
        model = Avatar
        fields = ['sticker']