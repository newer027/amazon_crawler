from django import forms
from .models import In_word


class In_word_Form(forms.ModelForm):

    class Meta:
        model = In_word
        fields = ('in_word','country',)