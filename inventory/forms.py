from django import forms
from .models import Inventory


class Inventory_Form(forms.ModelForm):

    class Meta:
        model = Inventory
        fields = ('asin','country',)