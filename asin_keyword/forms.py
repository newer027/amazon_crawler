from django import forms
from .models import Asin_keyword


class Asin_keyword_Form(forms.ModelForm):

    class Meta:
        model = Asin_keyword
        fields = ('asin','country',)
