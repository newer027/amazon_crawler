from django import forms
from .models import Shorten_Url


class Shorten_Url_Form(forms.ModelForm):
    seller = forms.CharField(required=False)

    class Meta:
        model = Shorten_Url
        fields = ('asin','seller','country','keywords',)

