from django import forms
from core.models import Product


class Asin_detail_Form(forms.ModelForm):

    class Meta:
        model = Product
        fields = ('country','asins_in',)
