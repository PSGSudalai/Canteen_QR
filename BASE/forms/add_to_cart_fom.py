# BASE/forms.py

from django import forms
from BASE.models import CanteenItems, Cart


class AddToCartForm(forms.Form):
    item = forms.ModelChoiceField(queryset=CanteenItems.objects.all())
    quantity = forms.IntegerField(min_value=1, initial=1)
