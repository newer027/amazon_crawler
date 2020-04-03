from django import forms
from .models import Keyword_rank


class Keyword_rank_Form(forms.ModelForm):

    class Meta:
        model = Keyword_rank
        fields = ('asin','country','word')

