from django import forms
from .models import MorningMessage

class PasswordForm(forms.Form):
    password = forms.CharField(label='Your password', max_length=10,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                 'autofocus':'autofocus',
                                                                 'size': '6', 'autocomplete':'off'}),)



class MorningMessageForm(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea(attrs={'cols': 10, 'rows': 2}))
    class Meta:
        model = MorningMessage
        fields = ['date', 'message']

