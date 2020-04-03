from django import forms
from .models import Url_to_wishlist


class Url_to_wishlist_Form(forms.ModelForm):

    class Meta:
        model = Url_to_wishlist
        fields = ('url',)